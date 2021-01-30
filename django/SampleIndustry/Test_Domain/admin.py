from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from Test_Domain.models import Country

from Test_Domain.models import Department

from Test_Domain.models import Employee

from Test_Domain.models import JobHistory

from Test_Domain.models import Location

from Test_Domain.models import Region



class CountryInline(admin.TabularInline):
    model = Country





    

class DepartmentInline(admin.TabularInline):
    model = Department





    

class EmployeeInline(admin.TabularInline):
    model = Employee





    

class JobHistoryInline(admin.TabularInline):
    model = JobHistory




    

class LocationInline(admin.TabularInline):
    model = Location





    

class RegionInline(admin.TabularInline):
    model = Region




    


class CountryAdmin(admin.ModelAdmin):
	inlines = [
	
	]


class DepartmentAdmin(SimpleHistoryAdmin):
	inlines = [
	LocationInline,
	]


class EmployeeAdmin(admin.ModelAdmin):
	inlines = [DepartmentInline,
	
	]


class JobHistoryAdmin(admin.ModelAdmin):
	inlines = [
	EmployeeInline,
	]


class LocationAdmin(admin.ModelAdmin):
	inlines = [
	
	]


class RegionAdmin(admin.ModelAdmin):
	inlines = [CountryInline,
	
	]



admin.site.register(Country, CountryAdmin)

admin.site.register(Department, DepartmentAdmin)

admin.site.register(Employee, EmployeeAdmin)

admin.site.register(JobHistory, JobHistoryAdmin)

admin.site.register(Location, LocationAdmin)

admin.site.register(Region, RegionAdmin)

