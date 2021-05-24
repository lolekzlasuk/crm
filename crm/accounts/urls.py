from django.urls import path

from . import views
app_name = 'accounts'
urlpatterns = [
    path('employees/',views.EmployeeListView.as_view(),name="employees"),
    path('login/',views.user_login,name='user_login'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('profile',views.UserProfileDetailView.as_view(),name='profile'),
    path('profile/edit',views.edit_profile,name='edit_profile'),
    path('profile/password/', views.change_password, name='change_password'),
    path('profile/profile_pic_default',views.delete_profile_pic,name='delete_profile_pic')
    # path('employees/search/',views.EmployeeSearchListView.as_view(),name="search_employees"),


    # path('profile/',views.EmployeeDetailView.as_view(),name="profile"),
]
