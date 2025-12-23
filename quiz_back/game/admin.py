from django.contrib import admin
from .models import ProblemSet, Map, ProblemSetQuestion, PlaySession, SessionLog

# 문제집 문제 추가 관련 클래스
class ProblemSetQuestionInline(admin.TabularInline):
    model = ProblemSetQuestion
    extra = 1
    autocomplete_fields = ['problem']  # 문제 선택시 검색 가능 (선택사항)

class ProblemSetAdmin(admin.ModelAdmin):
    inlines = [ProblemSetQuestionInline]

# 게임맵 문제집 추가 관련 클래스
class MapAdmin(admin.ModelAdmin):
    filter_horizontal = ['problem_sets']

admin.site.register(ProblemSet, ProblemSetAdmin)
admin.site.register(Map, MapAdmin)
admin.site.register(PlaySession)
admin.site.register(SessionLog)