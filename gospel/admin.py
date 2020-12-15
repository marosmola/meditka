from django.contrib import admin
from .models import Day, Gospel, Reading, Psalm


class GospelInline(admin.StackedInline):
    model = Gospel
    extra = 0


class DayAdmin(admin.ModelAdmin):
    inlines = [
        GospelInline,
    ]
    search_fields = ['date']


admin.site.register(Day, DayAdmin)
# admin.site.register(Gospel)
admin.site.register(Reading)
admin.site.register(Psalm)
