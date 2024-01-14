from django.urls import path
from .views import *
from django.contrib import messages
urlpatterns = [
    path('adduser/',AddUser,name="AddUser"),
    path('user/',user.as_view(),name="User"),
    path('edit/<id>',user.update,name="edit"),
    path('login/',Login.as_view(),name="login"),
    path('logedin/',Login.Login,name="Logedin"),
    path('logout/',views.LogoutView.as_view(
        next_page=None,
        template_name='accounts/logout.html'
    ),name="logout"),
]