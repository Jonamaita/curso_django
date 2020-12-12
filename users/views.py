"""
User Views
"""

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
# Models
from django.contrib.auth.models import User
# Redirect nos ayudara a redireccionarnos a otro path
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView

from posts.models import Post
# Forms
# Importamos el ProfileForm que creamos anteriormente
from users.forms import SignupForm
from users.models import Profile


class UserDetailView(LoginRequiredMixin, DetailView):
    """User detail view."""

    template_name = "users/detail.html"

    # Es el campo que se la pasara a la query para buscar el usuario
    # Podemos pasarle <email> tambien, esta vez buscamos el usuario por su
    # username
    slug_field = "username"

    # Es la palabra clave que le pasamos al url detail/<str:username>/
    slug_url_kwarg = "username"

    queryset = User.objects.all()

    # Esto es como se mandara el objeto al html
    context_object_name = "user"

    # Sobre escribimos el método get_context_data para mandar el listado de
    # posts. get_context_data siempre agrega contexto al html.
    def get_context_data(self, **kwargs):
        """Add user's posts to context."""
        # nos traemos el contexto de original de la clase padre.
        context = super().get_context_data(**kwargs)

        # get_object busca un pk_url_kwargargumento en los argumentos de la
        # vista, si se encuentra este argumento, este método realiza una
        # búsqueda basada en clave primaria utilizando ese valor.
        user = self.get_object()

        # Agregamos contexto posts
        context["posts"] = Post.objects.filter(user=user).order_by("-created")
        return context


class LoginView(auth_views.LoginView):
    """Login view."""

    template_name = 'users/login.html'
    # Si un usuario loguenado entra en login, lo redirige a la url de la
    # variable LOGIN_REDIRECT_URL definida en settings
    redirect_authenticated_user = True


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Update profile view."""

    template_name = "users/update_profile.html"
    model = Profile
    fields = ["website", "biography", "phone_number", "picture"]

    def get_object(self):
        """Return user's profile."""
        # Retorna el objeto profile
        return self.request.user.profile

    def get_success_url(self):
        """Return to user's profile."""

        # self.obejct es el profile que retornamos en get_object
        username = self.object.user.username

        return reverse("users:detail", kwargs={"username": username})


class SignupView(FormView):
    """
    Signup View.
    """

    template_name = "users/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)
