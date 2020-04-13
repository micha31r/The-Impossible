from django.urls import path

from .views import (
	signup_page,
	login_page,
	logout_view,
)

urlpatterns = [
	path('signup/', signup_page, name="signup_page"),
	path('login/', login_page, name="login_page"),
	path('logout/', logout_view, name="logout_view"),
]