from django.contrib import admin
from .models import Station, Coordinates, Command


class CoordinatesInlines(admin.StackedInline):
    model = Coordinates


class StationsAdmin(admin.ModelAdmin):
    inlines = [CoordinatesInlines]

    list_display = (
        'name',
        'status',
        'create_date',
        'brake_date',
        'coordinates'
    )


admin.site.register(Station, StationsAdmin)
admin.site.register(Coordinates)
admin.site.register(Command)
