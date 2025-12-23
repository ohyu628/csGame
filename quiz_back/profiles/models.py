from django.db import models
from django.conf import settings
from questions.models import Category 

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    # (선택) 프로필에서 별도 표시명을 쓰고 싶으면 nickname으로 명확히 분리하는 게 좋음
    # 기존 username 필드를 유지하고 싶으면 아래 nickname은 빼도 됨.
    nickname = models.CharField(max_length=50, unique=True, null=True, blank=True)

    level = models.PositiveIntegerField(default=1)
    experience = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_experience = models.PositiveIntegerField(default=0, db_index=True)

    def __str__(self):
        # nickname이 있으면 nickname, 없으면 user.username
        display = self.nickname or self.user.username
        return f"{display} ({self.user.username})"

    def add_experience(self, amount: int):
        if amount <= 0:
            return

        self.total_experience += amount
        self.experience += amount

        while self.experience >= self.level * 100:
            self.experience -= self.level * 100
            self.level += 1

        self.save(update_fields=["total_experience", "experience", "level", "updated_at"])
    
class UserStats(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stats"
    )

    total_solved = models.PositiveIntegerField(default=0)
    total_correct = models.PositiveIntegerField(default=0)
    total_wrong = models.PositiveIntegerField(default=0)

    last_solved_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def accuracy(self):
        return 0.0 if self.total_solved == 0 else (self.total_correct / self.total_solved)

    def __str__(self):
        return f"Stats({self.user_id})"
    


class UserCategoryStats(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="category_stats"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="user_stats"
    )

    solved = models.PositiveIntegerField(default=0)
    correct = models.PositiveIntegerField(default=0)
    wrong = models.PositiveIntegerField(default=0)

    last_solved_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "category"], name="uniq_user_category_stats")
        ]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["category"]),
        ]

    @property
    def accuracy(self):
        return 0.0 if self.solved == 0 else (self.correct / self.solved)

    def __str__(self):
        return f"CatStats(u={self.user_id}, c={self.category_id})"
