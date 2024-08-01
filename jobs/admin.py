from django.contrib import admin
from .models import Category, ContractType, Job

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(ContractType)
class ContractTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'contract_type', 'location', 'created_date', 'deadline', 'posted_by')
    search_fields = ('title', 'location', 'description')
    list_filter = ('category', 'contract_type', 'created_date', 'deadline')
    raw_id_fields = ('posted_by',)