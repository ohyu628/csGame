from django.contrib import admin
from .models import Problem, Category

# 어드민 사이트에서 문제 추가시 문제로 검색가능
@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    search_fields = ['question',] 

admin.site.register(Category)
# admin.site.register(Problem)
