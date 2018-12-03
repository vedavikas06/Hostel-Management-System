from django.contrib import admin
from .models import *


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'student_name',
        'father_name',
        'gender',
        'enrollment_no',
        'course',
        'dob',
        'room',
        'room_allotted']
    actions = ["delete_selected"]

    def delete_selected(self, request, queryset):
        for element in queryset:
            element.delete()

    delete_selected.short_description = "Delete selected elements"


# class ElementAdmin(admin.ModelAdmin):
#     class Meta:
#         actions = ["delete_selected"]
#
#         def delete_selected(self, request, queryset):
#             for element in queryset:
#                 element.delete()
#
#         delete_selected.short_description = "Delete selected elements"


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['no', 'name', 'room_type', 'vacant', 'hostel']
    actions = ["delete_selected"]

    def delete_selected(self, request, queryset):
        for element in queryset:
            element.delete()

    delete_selected.short_description = "Delete selected elements"



@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'room_type']


@admin.register(User)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['is_warden','username']


@admin.register(Warden)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'username']
    actions = ["delete_selected"]

    def username(self, obj):
        return obj.user.username

    def delete_selected(self, request, queryset):
        for element in queryset:
            element.delete()

    delete_selected.short_description = "Delete selected elements"


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ['student','start_date','end_date','reason','accept','reject','confirm_time']