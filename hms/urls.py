from django.contrib import admin
from django.urls import path
from selection import views
from django.conf.urls import include, url
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^', include(('selection.urls', 'selection'), namespace='selection')),
    url(r'^guest/', include('guest.urls', namespace='guest')),
    path('', views.start, name='start'),
    path('hms/', views.home, name='register'),
    path('reg_form/', views.register, name='reg_form'),
    path('login/', views.user_login, name='login'),
    path('student_profile/', views.student_profile, name='student_profile'),
    path('warden_login/', views.warden_login, name='warden_login'),
    path('warden_login/leave', views.leave_admin, name='leave_admin'),
    path('warden_login/student_leaves/<int:std_id>/', views.student_leaves, name='student_leaves'),
    path('warden_login/leave_confirm/<int:lv_id>/', views.leave_confirm, name='leave_confirm'),
    path('warden_login/leave_reject/<int:lv_id>/', views.leave_reject, name='leave_reject'),
    path('warden_login/empty/', views.empty_rooms, name='empty_rooms'),
    path('warden_login/present_leaves/', views.present_leaves, name='present_leaves'),
    path('warden_login/mess_rebate/', views.mess_rebate, name='mess_rebate'),
    path('warden_login/guest_requests/', views.guest_requests, name='guest_requests'),
    path('warden_login/bookings/<int:b_id>/', views.bookings, name='bookings'),
    path('warden_login/confirm/<int:res_id>/', views.guest_accept, name='guest_accept'),
    path('warden_login/cancel/<int:res_id>/', views.guest_reject, name='guest_reject'),
    path('warden_profile/', views.warden_profile, name='warden_profile'),
    path('warden_dues/', views.warden_dues, name='warden_dues'),
    path('warden_add_due/', views.warden_add_due, name='warden_add_due'),
    path('warden_remove_due/', views.warden_remove_due, name='warden_remove_due'),
    path('hostels/', views.hostels, name='hostel_all'),
    path('hostels/<slug:hostel_name>/', views.hostel_detail_view, name='hostel'),
    path('login/edit/', views.edit, name='edit'),
    path('login/select/', views.select, name='select'),
    path('login/repair/', views.repair, name='repair'),
    path('logout/', views.logout_view, name='logout'),
    path('reg_form/login/edit/', views.edit, name='update'),
    path('BH5_GroundFloor/', views.BH5_GroundFloor, name='BH5_GroundFloor'),
    path('BH5_Floor1/', views.BH5_Floor1, name='BH5_Floor1'),
    path('BH5_Floor2/', views.BH5_Floor2, name='BH5_Floor2'),
    path('BH5_Floor3/', views.BH5_Floor3, name='BH5_Floor3'),
    path('BH5_Floor4/', views.BH5_Floor4, name='BH5_Floor4'),
    path('BH5_Floor5/', views.BH5_Floor5, name='BH5_Floor5'),
    path('BH5_Floor6/', views.BH5_Floor6, name='BH5_Floor6'),
    path('login/leave', views.user_leave, name='leave_status'),
]
