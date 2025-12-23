from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import QuestionSerializer 
from .models import Problem
from game.models import ProblemSet
from game.serializers import ProblemSetSerializer
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.db import transaction

# Create your views here.
# 개인 문제집 조회 및 문제집 프레임 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def problemset_create(request):
    if request.method == 'GET':
        problemsets = ProblemSet.objects.filter(created_by=request.user)
        serializer = ProblemSetSerializer(problemsets, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProblemSetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# 문제집 상세 페이지, 수정, 삭제    
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def problemset_detail(request, set_pk):

    # ✅ GET은 누구나 조회 가능 (로그인 유저 기준)
    qs = ProblemSet.objects.annotate(problem_count=Count('problem', distinct=True))
    problemset = get_object_or_404(qs, pk=set_pk)

    if request.method == 'GET':
        return Response(ProblemSetSerializer(problemset).data)

    # ✅ 수정/삭제는 작성자만
    if problemset.created_by != request.user:
        return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PATCH':
        serializer = ProblemSetSerializer(problemset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # created_by는 serializer에서 read_only로 막는 게 안전
        return Response(serializer.data)

    if request.method == 'DELETE':
        problemset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# 문제집 안 문제들에 대한 조회 및 수정 삭제
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def problemset_problems(request, set_pk):
    # 문제집 존재 여부 + 유저 소유권 체크
    try:
        problemset = ProblemSet.objects.get(pk=set_pk, created_by=request.user)
    except ProblemSet.DoesNotExist:
        return Response({"detail": "문제집을 찾을 수 없습니다."}, status=404)

    # 1) 문제 리스트 조회
    if request.method == 'GET':
        problems = problemset.problem.all()
        serializer = QuestionSerializer(problems, many=True)
        return Response(serializer.data)

    # 2) 문제 생성 + 문제집 자동 추가
    elif request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():
            # 문제 생성 (유저 소유 문제)
            new_problem = serializer.save(created_by=request.user)
            # 문제집에 포함
            problemset.problem.add(new_problem)

            return Response({
                "detail": "문제 생성 완료",
                "problem": QuestionSerializer(new_problem).data
            }, status=201)

        return Response(serializer.errors, status=400)

    # 3) 문제 삭제 (문제집에서만 제거됨)
    elif request.method == 'DELETE':
        problem_id = request.data.get("problem_id")

        if not problem_id:
            return Response({"detail": "problem_id는 필수입니다."}, status=400)

        try:
            problem = Problem.objects.get(id=problem_id, created_by=request.user)
        except Problem.DoesNotExist:
            return Response({"detail": "해당 문제를 찾을 수 없거나 권한이 없습니다."}, status=404)

        problem.delete()

        return Response({"detail": "문제 삭제 완료"}, status=200)



@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def problem_detail(request, problem_pk):
    problem = get_object_or_404(Problem, pk=problem_pk)

    # ✅ GET: 로그인만 하면 조회 (원하면 공개로 바꿀 수 있음)
    if request.method == "GET":
        return Response(QuestionSerializer(problem).data)

    # ✅ PATCH/DELETE: "이 문제를 포함하는 문제집 중 내가 만든 문제가 있는가?"로 권한 체크
    # (문제가 여러 문제집에 걸려 있을 수 있으니 가장 안전)
    owns_any_linked_problemset = ProblemSet.objects.filter(
        created_by=request.user,
        problem=problem,
    ).exists()

    if not owns_any_linked_problemset:
        return Response({"detail": "권한이 없습니다."}, status=403)

    if request.method == "PATCH":
        serializer = QuestionSerializer(problem, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # DELETE: 문제 자체 삭제 (주의: 다른 문제집에서도 사라짐)
    if request.method == "DELETE":
        problem.delete()
        return Response(status=204)