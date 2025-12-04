from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API Router
router = DefaultRouter()
router.register(r'profiles', views.ProfileViewSet, basename='profile')
router.register(r'rides', views.RideViewSet, basename='ride')
router.register(r'polls', views.PollViewSet, basename='poll')

app_name = 'club'

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Frontend views
    path('', views.home, name='home'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('rides/', views.rides_list, name='rides_list'),
    path('rides/<int:pk>/', views.ride_detail, name='ride_detail'),
    path('upcoming-ride/', views.upcoming_ride, name='upcoming_ride'),
    path('rides/add/', views.ride_add, name='ride_add'),
    path('rides/<int:pk>/edit/', views.ride_edit, name='ride_edit'),
    path('rides/<int:pk>/join/', views.ride_join, name='ride_join'),
    path('rides/<int:pk>/leave/', views.ride_leave, name='ride_leave'),
    path('rides/<int:pk>/complete/', views.ride_mark_complete, name='ride_mark_complete'),
    path('polls/', views.poll_list, name='poll_list'),
    path('members/', views.members_list, name='members_list'),
    path('members/add/', views.member_add, name='member_add'),
    path('members/<int:user_id>/delete/', views.member_delete, name='member_delete'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
