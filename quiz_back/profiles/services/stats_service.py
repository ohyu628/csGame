# profiles/services/stats_service.py
from django.db.models import F
from django.utils import timezone

from profiles.models import UserStats, UserCategoryStats

def update_stats_from_log(log):
    """
    SessionLog 1건 생성 직후 호출:
    - UserStats / UserCategoryStats 카운트 증가
    """
    user = log.user
    problem = log.problem
    solved_at = log.solved_at or timezone.now()

    # ✅ 1) 유저 전체 통계
    UserStats.objects.get_or_create(user=user)
    UserStats.objects.filter(user=user).update(
        total_solved=F("total_solved") + 1,
        total_correct=F("total_correct") + (1 if log.is_correct else 0),
        total_wrong=F("total_wrong") + (0 if log.is_correct else 1),
        last_solved_at=solved_at,
    )

    # ✅ 2) 카테고리별 통계 (카테고리 없으면 스킵)
    if problem.category_id:
        UserCategoryStats.objects.get_or_create(user=user, category_id=problem.category_id)
        UserCategoryStats.objects.filter(user=user, category_id=problem.category_id).update(
            solved=F("solved") + 1,
            correct=F("correct") + (1 if log.is_correct else 0),
            wrong=F("wrong") + (0 if log.is_correct else 1),
            last_solved_at=solved_at,
        )
