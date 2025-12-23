from django.db import models
from django.conf import settings
from questions.models import Problem
from django.utils import timezone
# 문제집 테이블
class ProblemSet(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)    # 생성 시간
    updated_at = models.DateTimeField(auto_now=True)    # 수정 시간
    created_by = models.ForeignKey(     # 만든 유저 왜래키
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,      # 유저가 삭제돼도 문제집은 남김
        null=True,                       # 필수값 X
        blank=True,                      # admin 폼에서도 optional
        related_name="created_problem_sets",  # User.created_problem_sets로 User에서 접근 가능
        verbose_name="작성자"
    )
    problem = models.ManyToManyField( # 문제 M:N 참조
        'questions.Problem',  # questions 앱에 있는 Question 모델
        through='ProblemSetQuestion', # 기본 M:N 테이블 대신 스루 테이블 생성
        related_name='problem_sets' # 역참조 이름 설정
    )
    like_users = models.ManyToManyField(    # 좋아요, 유저 테이블 M:N 참조
        settings.AUTH_USER_MODEL,   
        related_name='liked_problem_sets',
        blank=True
    )
    created_by_admin = models.BooleanField(default = False) # 운영자 생성 여부
    class Meta:
        ordering = ['-created_at']  # 최신 문제집 우선
        verbose_name = "문제집"
        verbose_name_plural = "문제집 목록"
        
    def __str__(self):
        return self.title  

# 문제 x 문제집 중개 스루 테이블
class ProblemSetQuestion(models.Model):
    problem_set = models.ForeignKey(ProblemSet, on_delete=models.CASCADE) 
    problem = models.ForeignKey('questions.Problem', on_delete=models.CASCADE)
    # order = models.PositiveIntegerField(null=True, blank=True)
    class Meta:
        unique_together = ('problem_set', 'problem') # 문제집 문제 중복 방지
        # ordering = ['order']  # order 기준 기본 정렬

# 게임 맵 테이블
class Map(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)    # 생성 시간
    updated_at = models.DateTimeField(auto_now=True)    # 수정 시간

    problem_sets = models.ManyToManyField(  # 문제집과 M:N 참조
        ProblemSet, 
        related_name='maps',  # 문제집에서 역참조: 문제집.maps
        blank=True
    )
    def __str__(self):
        return self.name

# 플레이 세션 모델
class PlaySession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="play_sessions"
    )

    problem_set = models.ForeignKey(
        ProblemSet,
        on_delete=models.CASCADE,
        related_name="play_sessions"
    )

    # 이번 세션에서 플레이할 문제들 (10개)
    selected_problems = models.ManyToManyField(
        Problem,
        related_name="play_sessions",
        blank=True
    )

    total_problems = models.PositiveIntegerField(default=10)  # 기본 10문제
    solved_count = models.PositiveIntegerField(default=0)      # 유저가 푼 문제 수
    is_completed = models.BooleanField(default=False)

    # 세션 시간 정보
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # 사용자가 도중에 나가거나 만료(예: 30분 후) 처리 가능
    expired = models.BooleanField(default=False)

    def __str__(self):
        return f"[PlaySession #{self.id}] {self.user.username} - {self.problem_set.title} ({self.solved_count}/{self.total_problems})"

    @property
    def is_completed_now(self):
        answered_count = SessionLog.objects.filter(session=self).count()
        return answered_count >= self.total_problems

    def mark_completed(self):
        """세션 완료 처리 함수"""
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save()

# 세션 히스토리 로그 모델
class SessionLog(models.Model):
    """
    플레이 중 사용자가 문제를 어떻게 풀었는지를 기록하는 모델
    - 세션별 문제 풀이 히스토리
    - AI 분석 및 오답 노트 기반 데이터
    """
    
    # 해당 유저
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="problem_logs"
    )

    # 해당 세션
    session = models.ForeignKey(
        "PlaySession",
        on_delete=models.CASCADE,
        related_name="logs"
    )

    # 어떤 문제를 풀었는지
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="logs"
    )

    # 유저가 제출한 답(정수형)
    selected_answer = models.IntegerField()

    # 정답 여부
    is_correct = models.BooleanField()

    # 문제 푸는 데 걸린 시간 (optional, 추후 집중도 분석)
    response_time_ms = models.PositiveIntegerField(null=True, blank=True)

    # 제출 시각
    solved_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("session", "problem")

        ordering = ["-solved_at"]
        verbose_name = "문제 풀이 로그"
        verbose_name_plural = "문제 풀이 로그들"

        # ✅ 인덱스 추가
        indexes = [
            # 유저의 최신 로그 조회 (프로필/히스토리)
            models.Index(fields=["user", "-solved_at"], name="idx_log_user_time"),

            # 최근 7일 오답 조회(너가 이미 쓰는 쿼리)
            models.Index(fields=["user", "is_correct", "-solved_at"], name="idx_log_user_wrong_time"),

            # 세션별 로그 조회 (세션 결과/리플레이)
            models.Index(fields=["session"], name="idx_log_session"),

            # 문제별 통계 집계/분석 (문제 단위 히트맵 같은 거 할 때)
            models.Index(fields=["problem"], name="idx_log_problem"),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.problem_id} - Correct:{self.is_correct}"