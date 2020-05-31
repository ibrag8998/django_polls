from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'pub_date', 'is_recent')
    list_filter = ('pub_date', )
    search_fields = ('text', )
    fieldsets = [
        ('General', {
            'fields': ['text']
        }),
        ('Date and Time', {
            'fields': ['pub_date']
        }),
    ]
    inlines = [ChoiceInline]


admin.AdminSite.site_title = admin.AdminSite.site_header = 'Admin Panel'

admin.site.register(Question, QuestionAdmin)
