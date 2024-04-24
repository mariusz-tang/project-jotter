from django.contrib.auth import views


class LoginView(views.LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True
