from django.contrib import admin
from schools.buildings.models import Building, Classroom, BuildingMonthExpense

admin.site.register(Building)
admin.site.register(Classroom)
admin.site.register(BuildingMonthExpense)