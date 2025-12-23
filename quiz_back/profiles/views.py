from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model


from questions.models import Category
from .models import Profile, UserStats, UserCategoryStats
from .serializers import UserProfileSerializer, UserStatsSerializer, UserCategoryStatsSerializer, RankingItemSerializer


User = get_user_model()

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """
    로그인한 유저의 현재 프로필 정보를 반환
    (user store fetchUser 용)
    """
    profile, _ = Profile.objects.get_or_create(user=request.user)
    serializer = UserProfileSerializer(profile)
    return Response(serializer.data)


def _build_payload(target_user):
    profile, _ = Profile.objects.get_or_create(user=target_user)
    stats, _ = UserStats.objects.get_or_create(user=target_user)

    # ✅ 유저가 가진 카테고리 통계를 dict로
    user_stats_qs = (
        UserCategoryStats.objects
        .filter(user=target_user)
        .select_related("category")
    )
    by_cat_id = {ucs.category_id: ucs for ucs in user_stats_qs}

    # ✅ 모든 카테고리를 순회하며 없으면 0으로 생성(조회만 할 거면 create 안 하고 임시로 만들기)
    all_categories = Category.objects.all().order_by("id")

    merged = []
    for c in all_categories:
        ucs = by_cat_id.get(c.id)
        if ucs:
            merged.append(ucs)
        else:
            # DB에 저장할 필요 없으면 메모리 객체로 0값 생성
            merged.append(UserCategoryStats(user=target_user, category=c, solved=0, correct=0, wrong=0))

    cat_data = UserCategoryStatsSerializer(merged, many=True).data

    return {
        "user": {"id": target_user.id},
        "profile": UserProfileSerializer(profile).data,
        "stats": UserStatsSerializer(stats).data,
        "category_stats": cat_data,   # ✅ 모든 카테고리 포함(0점 포함)
    }


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_profile_stats(request):
    """
    내 프로필 + 통계 + 카테고리 숙련도 + 요약
    """
    return Response(_build_payload(request.user), status=200)


@api_view(["GET"])
@permission_classes([AllowAny])  # ✅ 공개로 할지, IsAuthenticated로 할지 선택 가능
def user_profile_stats(request, user_id: int):
    """
    다른 유저 프로필/통계 조회
    """
    try:
        target = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status=404)

    return Response(_build_payload(target), status=200)

def _rank_ordering():
    # 동점 기준까지 고정 정렬 (반드시 동일하게 사용)
    return ["-total_experience", "-level", "-experience", "user_id"]

def _count_better_than(me: Profile) -> int:
    """
    me 보다 '랭킹이 높은' Profile 개수
    (total_exp, level, exp, user_id 기준)
    """
    return Profile.objects.filter(
        Q(total_experience__gt=me.total_experience)
        | (
            Q(total_experience=me.total_experience)
            & Q(level__gt=me.level)
        )
        | (
            Q(total_experience=me.total_experience)
            & Q(level=me.level)
            & Q(experience__gt=me.experience)
        )
        | (
            Q(total_experience=me.total_experience)
            & Q(level=me.level)
            & Q(experience=me.experience)
            & Q(user_id__lt=me.user_id)
        )
    ).count()

@api_view(["GET"])
@permission_classes([AllowAny])
def ranking(request):

    try:
        limit = int(request.query_params.get("limit", 50))
    except ValueError:
        limit = 50

    limit = max(1, min(limit, 200))  # 과도한 요청 방지

    qs = (
        Profile.objects
        .select_related("user")
        .order_by(*_rank_ordering())
    )

    top = list(qs[:limit])
    top_data = RankingItemSerializer(top, many=True).data

    # top 리스트에 rank 부여 (동점 고려해서 "진짜 등수" 계산)
    # - limit이 작으니 각 아이템당 count 쿼리 발생해도 부담 적음
    items = []
    for p, row in zip(top, top_data):
        rank_num = _count_better_than(p) + 1
        items.append({**row, "rank": rank_num})

    me_payload = None
    if request.user.is_authenticated:
        me, _ = Profile.objects.get_or_create(user=request.user)
        me_rank = _count_better_than(me) + 1
        me_payload = {
            **RankingItemSerializer(me).data,
            "rank": me_rank,
        }

    return Response({
        "limit": limit,
        "items": items,
        "me": me_payload,
    })