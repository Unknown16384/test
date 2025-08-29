from django.contrib import admin

from .models import UserProfile, Skills, SkillList, Gallery, Desks

class SkillInLine(admin.StackedInline):
    model = Skills
    extra = 0

class ImageInLine(admin.StackedInline):
    model = Gallery
    extra = 0

@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'all_skills', 'desk__number')
    inlines = (SkillInLine, ImageInLine)

    def full_name(self, obj):
        return f'{obj.family} {obj.name} {obj.surname}'
    full_name.short_description = 'ФИО'
    def all_skills(self, obj):
        return list(Skills.objects.filter(user_id=obj.id))
    all_skills.short_description = 'Навыки'

admin.site.register(SkillList)
admin.site.register(Desks)