from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

# 카테고리 모델
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 카테고리 명
    description = models.TextField(blank=True, null=True)  # 카테고리 설명 (선택사항)

    def __str__(self):
        return self.name

# 문제 모델
class Problem(models.Model):

    question = models.TextField(max_length=500)   # 문제 (필수)
    choice1 = models.CharField(max_length=255)  # 객관식 항목 1~4 (필수)
    choice2 = models.CharField(max_length=255)
    choice3 = models.CharField(max_length=255)
    choice4 = models.CharField(max_length=255)
    
    # 정답 (필수)
    answer = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)],
    help_text="정답 선택지 번호 (1~4)"
    )

    explanation = models.TextField(blank=True, default='')  # 설명 (필수X, 기본값 "")

    created_at = models.DateTimeField(auto_now_add=True)    # 생성 시간
    updated_at = models.DateTimeField(auto_now=True)    # 수정 시간

    created_by_admin = models.BooleanField(default = False) # 운영자 생성 여부

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_problems",
        verbose_name="작성자"
    )

    # 난이도 선택지
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'
    DIFFICULTY_CHOICES = [
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard'),
    ]

    # 난이도 필드
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default=EASY,
        help_text="문제 난이도"
    )

    # 카테고리 필드
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,  # 카테고리가 삭제되도 문제는 유지
        null=True,
        blank=True,
        related_name='problems'
    )
    
    def __str__(self):
        return self.question
