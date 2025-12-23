import math
from rest_framework import serializers
from .models import Profile, UserCategoryStats, UserStats

class UserProfileSerializer(serializers.ModelSerializer):
    # ✅ Profile에 username 필드가 없으니 user.username을 내려주기
    username = serializers.CharField(source="user.username", read_only=True)

    # ✅ 프론트에서 exp로 쓰는 키 유지
    exp = serializers.IntegerField(source="experience", read_only=True)

    max_exp = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "username",
            "level",
            "exp",
            "max_exp",
        ]

    def get_max_exp(self, obj):
        return obj.level * 100
    
class UserStatsSerializer(serializers.ModelSerializer):
    accuracy = serializers.SerializerMethodField()
    accuracy_pct = serializers.SerializerMethodField()

    class Meta:
        model = UserStats
        fields = [
            "total_solved",
            "total_correct",
            "total_wrong",
            "accuracy",
            "accuracy_pct",
            "last_solved_at",
            "updated_at",
        ]

    def get_accuracy(self, obj):
        return 0.0 if obj.total_solved == 0 else (obj.total_correct / obj.total_solved)

    def get_accuracy_pct(self, obj):
        acc = self.get_accuracy(obj)
        return round(acc * 100, 1)


class UserCategoryStatsSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source="category.id", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    accuracy = serializers.SerializerMethodField()
    accuracy_pct = serializers.SerializerMethodField()
    proficiency_score = serializers.SerializerMethodField()

    class Meta:
        model = UserCategoryStats
        fields = [
            "category_id",
            "category_name",
            "solved",
            "correct",
            "wrong",
            "accuracy",
            "accuracy_pct",
            "proficiency_score",
            "last_solved_at",
            "updated_at",
        ]

    def get_accuracy(self, obj):
        return 0.0 if obj.solved == 0 else (obj.correct / obj.solved)

    def get_accuracy_pct(self, obj):
        return round(self.get_accuracy(obj) * 100, 1)

    def get_proficiency_score(self, obj):
        solved = obj.solved or 0
        correct = obj.correct or 0

        if solved <= 0:
            return 0.0

        smoothed = (correct + 2) / (solved + 4)          # 0~1
        confidence = 1 - math.exp(-solved / 20.0)        # 0~1
        score = 100.0 * smoothed * confidence            # 0~100

        return round(score, 1)
    
class RankingItemSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = Profile
        fields = ["user_id", "username", "level", "experience", "total_experience"]