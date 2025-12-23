from rest_framework import serializers
from .models import Map, ProblemSet
from questions.models import Problem
from .models import SessionLog

# 맵 목록 시리얼라이저
class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ('id', 'name', 'description',)

# 문제집 시리얼라이저
class ProblemSetSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    problem_count = serializers.IntegerField(read_only=True)  # ✅ 추가
    
    class Meta:
        model = ProblemSet
        fields = ('id', 'title', 'description', 'like_count', 'created_by', 'created_by_name', 'problem_count', )
        read_only_fields = ['id','problem_count']
    def get_like_count(self, obj):
        return obj.like_users.count()
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.username  # 또는 이름 필드
        return None

# 맵 문제집 시리얼라이저
class MapProblemSetSerializer(serializers.ModelSerializer):

    problem_sets = ProblemSetSerializer(many=True, read_only=True)
    
    class Meta:
        model = Map
        fields = ('id', 'name', 'description', 'problem_sets',)

# 문제 보기용 시리얼라이저
class ProblemViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('id', 'question', 'choice1', 'choice2', 'choice3', 'choice4',)

# 문제집 문제 시리얼라이저 (보기용)
class ProblemSetProblemSerializer(serializers.ModelSerializer):

    questions = ProblemViewSerializer(many=True, read_only=True)

    class Meta:
        model = ProblemSet
        fields = ('id', 'title', 'description', 'problem',)


class RecentWrongLogSerializer(serializers.ModelSerializer):
    problem_id = serializers.IntegerField(source="problem.id", read_only=True)
    question = serializers.CharField(source="problem.question", read_only=True)

    choice1 = serializers.CharField(source="problem.choice1", read_only=True)
    choice2 = serializers.CharField(source="problem.choice2", read_only=True)
    choice3 = serializers.CharField(source="problem.choice3", read_only=True)
    choice4 = serializers.CharField(source="problem.choice4", read_only=True)

    correct_answer = serializers.IntegerField(source="problem.answer", read_only=True)
    explanation = serializers.CharField(source="problem.explanation", read_only=True)

    difficulty = serializers.CharField(source="problem.difficulty", read_only=True)

    category_id = serializers.IntegerField(source="problem.category.id", read_only=True, allow_null=True)
    category_name = serializers.CharField(source="problem.category.name", read_only=True, allow_null=True)

    class Meta:
        model = SessionLog
        fields = (
            "id",
            "solved_at",
            "response_time_ms",
            "selected_answer",
            "is_correct",
            "problem_id",
            "question",
            "choice1", "choice2", "choice3", "choice4",
            "correct_answer",
            "explanation",
            "difficulty",
            "category_id",
            "category_name",
        )
