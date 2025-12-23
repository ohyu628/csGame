from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

from game.models import SessionLog
from ai.services.ai_client import call_chat_completions, UpstreamAIError

def extract_chat_text(data: dict) -> str:
    try:
        return (data["choices"][0]["message"]["content"] or "").strip()
    except Exception:
        return ""

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ai_echo(request):
    user_input = request.data.get("input", "")
    if not user_input:
        return Response({"detail": "input is required"}, status=400)

    messages = [
        {"role": "developer", "content": "Answer in Korean."},
        {"role": "user", "content": user_input},
    ]

    try:
        raw = call_chat_completions(messages=messages)
        return Response({"output": extract_chat_text(raw)}, status=200)

    except UpstreamAIError as e:
        # 개발 중엔 원인 노출, 배포 시엔 숨김
        if settings.DEBUG:
            return Response(
                {"detail": "AI upstream error", "upstream_status": e.status_code, "upstream_body": e.detail},
                status=502,
            )
        return Response({"detail": "AI service unavailable"}, status=502)

    except Exception as e:
        # 진짜 서버 코드 버그
        if settings.DEBUG:
            return Response({"detail": f"Server error: {e}"}, status=500)
        return Response({"detail": "Server error"}, status=500)
    
def get_choice(problem, n: int) -> str:
    """
    n(1~4)에 해당하는 선택지 텍스트 반환
    """
    if n not in (1, 2, 3, 4):
        return "-"
    return getattr(problem, f"choice{n}", "-") or "-"


def pack_wrong_logs_for_ai(logs) -> str:
    """
    AI에 넣기 좋은 텍스트로 '최소' 압축:
    - category/difficulty
    - 문제 지문(짧게)
    - 내가 고른 보기 텍스트 / 정답 보기 텍스트
    """
    lines = []

    for i, log in enumerate(logs, start=1):
        p = log.problem
        category = p.category.name if p.category else "-"

        # 안전 변환
        try:
            selected = int(log.selected_answer)
        except Exception:
            selected = 0

        correct = int(p.answer)

        chosen_txt = get_choice(p, selected)[:80]
        correct_txt = get_choice(p, correct)[:80]

        lines.append(
            f"[{i}] {category}/{p.difficulty}\n"
            f"Q: {(p.question or '')[:160]}\n"
            f"chosen: {selected}) {chosen_txt}\n"
            f"correct: {correct}) {correct_txt}"
        )

    return "\n\n".join(lines)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def wrong_feedback(request):
    """
    최근 7일 오답 최대 30개를 AI에 보내 피드백 받기
    """
    # 옵션 파라미터(필요하면 프론트에서 조정 가능)
    days = int(request.data.get("days", 7))
    limit = int(request.data.get("limit", 20))
    limit = min(max(limit, 1), 20)  # ✅ 최대 20 고정

    since = timezone.now() - timedelta(days=days)

    # ✅ 본인 + 최근 7일 + 오답만 + 최신순 + 최대 30
    logs = (
        SessionLog.objects
        .select_related("problem", "problem__category")
        .filter(user=request.user, is_correct=False, solved_at__gte=since)
        .order_by("-solved_at")[:limit]
    )

    if not logs:
        return Response(
            {"detail": "최근 7일 내 오답이 없습니다.", "count": 0, "from_days": days},
            status=200
        )

    packed = pack_wrong_logs_for_ai(logs)

    messages = [
        {
            "role": "developer",
            "content": (
                "너는 퀴즈 학습 코치다. 반드시 한국어로만 답해라.\n"
                "아래 오답 요약을 보고 '짧게' 피드백하라.\n"
                "규칙:\n"
                "- 전체 700~900자 이내\n"
                "- 섹션은 4개(1~4) 유지\n"
                "- 각 섹션은 최대 3개 bullet만\n"
                "- 불필요한 서론 금지, 바로 답만"
            )
        },
        {
            "role": "user",
            "content": f"최근 {days}일 오답 {len(logs)}개:\n\n{packed}"
        }
    ]

    try:
        raw = call_chat_completions(
            messages=messages,
            model="gpt-5",      # ✅ 필요하면 settings에서
            timeout=60
        )
        feedback_text = extract_chat_text(raw)

        return Response(
            {
                "count": len(logs),
                "from_days": days,
                "model": "gpt-5",
                "feedback": feedback_text,
            },
            status=200
        )

    except UpstreamAIError as e:
        # upstream 장애는 502로
        if settings.DEBUG:
            return Response(
                {"detail": "AI upstream error", "upstream_status": e.status_code, "upstream_body": e.detail},
                status=502
            )
        return Response({"detail": "AI service unavailable"}, status=502)