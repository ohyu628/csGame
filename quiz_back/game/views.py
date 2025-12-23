from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import Map, ProblemSet, PlaySession, SessionLog
from questions.models import Problem
from .serializers import (
    MapSerializer, 
    MapProblemSetSerializer, 
    ProblemSetSerializer,
    ProblemViewSerializer,
    RecentWrongLogSerializer,
)
from profiles.models import Profile
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from profiles.services.stats_service import update_stats_from_log
# ==================================================================================================
# 메인 모드 구현
# ==================================================================================================

# 맵 목록 호출
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def map_list(request):
    maps = Map.objects.all()
    serializer = MapSerializer(maps, many=True)
    return Response(serializer.data)

# 특정 맵 안에 존재하는 문제집 호출
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def map_detail(request, map_pk):
    maps = Map.objects.get(pk=map_pk)
    serializer = MapProblemSetSerializer(maps)
    return Response(serializer.data)

# 문제집 안 문제중 10문제 조회
# @api_view(['GET'])
# def problem_set_questions(request, problem_set_pk):
#     # 1. 문제집 불러오기
#     try:
#         problem_set = ProblemSet.objects.get(pk=problem_set_pk)
#     except ProblemSet.DoesNotExist:
#         return Response({"error": "ProblemSet not found"}, status=status.HTTP_404_NOT_FOUND)

#     # 2. 문제집 안의 문제들 가져오기
#     problems = problem_set.problem.all()  # 문제집에 연결된 모든 문제
#     # 3. 문제 10개만 랜덤으로 선택
#     problems = problems.order_by('?')[:10]  # '?'는 랜덤 정렬

#     # 4. 시리얼라이즈 후 반환
#     serializer = ProblemViewSerializer(problems, many=True)
#     return Response(serializer.data)

# 게임 플레이 세션 생성 및 문제 조회
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def start_play_session(request):
    problem_set_id = request.data.get("problem_set_id")

    if problem_set_id is None:
        return Response({"error": "problem_set_id는 필수값입니다."}, status=400)

    # 🧹 기존 0문제 세션 정리
    PlaySession.objects.filter(
        user=request.user,
        solved_count=0
    ).delete()

    # 문제집 조회
    try:
        problem_set = ProblemSet.objects.get(id=problem_set_id)
    except ProblemSet.DoesNotExist:
        return Response({"error": "해당 문제집이 존재하지 않습니다."}, status=404)

    # ✅ 문제 수 체크
    available_count = problem_set.problem.count()
    if available_count == 0:
        return Response({"error": "문제집에 문제가 없습니다."}, status=400)

    pick_count = min(10, available_count)  # ✅ 기본은 10, 부족하면 있는 만큼

    # 1) PlaySession 생성 (total_problems를 실제 뽑은 개수로)
    session = PlaySession.objects.create(
        user=request.user,
        problem_set=problem_set,
        total_problems=pick_count,
    )

    # 2) 문제집에서 문제 pick_count개 랜덤 선택
    problems = problem_set.problem.order_by("?")[:pick_count]

    # 세션에 문제 저장
    session.selected_problems.set(problems)

    # 3) 프론트에 반환할 데이터 구성
    serialized = ProblemViewSerializer(problems, many=True).data

    return Response({
        "session_id": session.id,
        "total_problems": pick_count,        # ✅ 프론트가 이걸 기준으로 진행하게
        "available_count": available_count,  # (선택) UI에 “현재 문제 수” 표시용
        "problems": serialized
    }, status=201)


  # ✅ 추가

# 퀴즈 정답 채점 함수
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic  # ✅ 추가
def check_answer(request):
    try:
        session_id = request.data.get("session_id")
        question_id = request.data.get("question_id")
        selected = request.data.get("selected")

        if session_id is None or question_id is None or selected is None:
            return Response(
                {"error": "session_id, question_id, selected는 필수값입니다."},
                status=400
            )

        # 🔐 세션 조회 & 유저 확인
        session = PlaySession.objects.get(id=session_id, user=request.user)

        if session.is_completed or session.expired:
            return Response({"error": "이미 종료된 세션입니다."}, status=400)

        # 문제 조회
        question = Problem.objects.get(id=question_id)

        # 🧩 이 문제가 이 세션에 포함된 문제인지 확인
        if question not in session.selected_problems.all():
            return Response({"error": "세션과 관련 없는 문제입니다."}, status=400)

        # 🎯 채점
        is_correct = (question.answer == int(selected))

        # 📝 즉시 SessionLog 저장
        try:
            log = SessionLog.objects.create(
                user=request.user,
                session=session,
                problem=question,
                selected_answer=int(selected),
                is_correct=is_correct,
                solved_at=timezone.now()
            )
        except IntegrityError:
            # unique_together ("session","problem") 때문에 같은 문제 재제출이면 여기로 옴
            return Response({"error": "이미 제출한 문제입니다."}, status=400)

        # ✅ 통계 업데이트(핵심 1줄)
        update_stats_from_log(log)

        # 몇번째 응답?
        # (성능상 session.logs.count() 추천. related_name="logs"라면 아래처럼 가능)
        answered_count = SessionLog.objects.filter(session=session).count()

        # 🔥 세션 상태 업데이트
        if is_correct:
            session.solved_count += 1

        session_completed_result = None

        if answered_count >= session.total_problems:
            session.mark_completed()

            correct = session.solved_count
            total = session.total_problems
            score = correct * 20

            profile, _ = Profile.objects.get_or_create(user=request.user)

            before_level = profile.level
            before_exp = profile.experience

            profile.add_experience(score)

            session_completed_result = {
                "score": score,
                "correct": correct,
                "total": total,
                "level_before": before_level,
                "level_after": profile.level,
                "before_exp": before_exp,
                "experience": profile.experience,
                "leveled_up": profile.level > before_level,
            }
        else:
            session.save()

        # 📡 응답 데이터 구성
        result = {
            "correct": is_correct,
            "correct_answer": question.answer,
            "explanation": question.explanation,
            "is_completed": session.is_completed,
            "solved_count": session.solved_count,
            "total_problems": session.total_problems,
            "session_result": session_completed_result
        }

        return Response(result, status=status.HTTP_200_OK)

    except PlaySession.DoesNotExist:
        return Response(
            {"error": "잘못된 session_id이거나 접근 권한이 없습니다."},
            status=status.HTTP_404_NOT_FOUND
        )

    except Problem.DoesNotExist:
        return Response(
            {"error": "해당 문제를 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND
        )


    # except Exception as e:
    #     return Response({"error": f"서버 오류: {str(e)}"},
    #                     status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# ==================================================================================================
# 유저 모드 구현
# ==================================================================================================

User = get_user_model()
@api_view(['GET'])
def user_problem_set(request, user_pk):
    # 1. 유저 존재 여부 확인
    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # 2. 해당 유저가 만든 문제집 조회
    problemsets = ProblemSet.objects.filter(created_by=user)
    
    # 3. 시리얼라이즈
    serializer = ProblemSetSerializer(problemsets, many=True)
    return Response(serializer.data)

# 유저 제작 문제집들을 조회
@api_view(['GET'])
def user_created_problem_set(request):

    problemsets = ProblemSet.objects.filter(created_by_admin=False)
    
    serializer = ProblemSetSerializer(problemsets, many=True)
    return Response(serializer.data)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def recent_wrong_logs(request):
    days = 7
    limit = 30
    since = timezone.now() - timedelta(days=days)

    qs = (
        SessionLog.objects
        .filter(
            user=request.user,
            is_correct=False,
            solved_at__gte=since,
        )
        .select_related("problem", "problem__category")  # ✅ 핵심
        .order_by("-solved_at")[:limit]
    )

    items = RecentWrongLogSerializer(qs, many=True).data

    # ✅ 난이도별 오답
    wrong_by_difficulty = (
        SessionLog.objects
        .filter(user=request.user, is_correct=False, solved_at__gte=since)
        .values("problem__difficulty")
        .annotate(cnt=Count("id"))
        .order_by("-cnt")
    )

    # ✅ 카테고리별 오답
    wrong_by_category = (
        SessionLog.objects
        .filter(user=request.user, is_correct=False, solved_at__gte=since)
        .values("problem__category_id", "problem__category__name")
        .annotate(cnt=Count("id"))
        .order_by("-cnt")
    )

    return Response({
        "window_days": days,
        "limit": limit,
        "count": len(items),
        "items": items,
        "stats": {
            "wrong_by_difficulty": list(wrong_by_difficulty),
            "wrong_by_category": list(wrong_by_category),
        }
    })