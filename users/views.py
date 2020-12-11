"""
User Views
"""

# Django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

# Models
from django.contrib.auth.models import User

# Redirect nos ayudara a redireccionarnos a otro path
from django.shortcuts import redirect, render
from django.views.generic import DetailView

from posts.models import Post

# Forms
# Importamos el ProfileForm que creamos anteriormente
from users.forms import ProfileForm, SignupForm


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


@login_required
def update_profile(request):
    """
    Update a user's profile view
    """
    # Crearemos una variable que guardara el profile
    # que esta realizando el request.
    profile = request.user.profile

    # Si el request es de tipo 'POST'
    if request.method == "POST":

        # Crearemos una instancia de ProfileForm
        # con los datos que recibimos a traves de request
        form = ProfileForm(request.POST, request.FILES)

        # Si la instacia se crea sin problemas.
        if form.is_valid():

            # Guardaremos los datos recibidos en base de datos.
            data = form.cleaned_data

            profile.website = data["website"]
            profile.phone_number = data["phone_number"]
            profile.biography = data["biography"]
            if data["picture"]:
                profile.picture = data["picture"]
            profile.save()

            # Y redireccionaremos a la pagina update_profile para reflejar los
            # cambios. Como detail, espera un argumento debemos usar reverse
            # y pasarle el argumento en los kwargs
            url = reverse(
                'users:detail',
                kwargs={'username': request.user.username},
            )
            return redirect(url)

    else:
        form = ProfileForm()

    return render(
        request=request,
        template_name="users/update_profile.html",
        # Enviaremos al template los datos del usuario.
        context={
            "profile": profile,
            "user": request.user,
            "form": form,
        },
    )


def login_view(request):
    """
    login view
    """

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # El metodo authenticate tratara de contrastar el usuario con una
        # instancia del modelo users que creamos.
        user = authenticate(request, username=username, password=password)
        if user:
            # En caso de ser exitoso la autenticación creara un token de
            # nuestro usuario para almacenarlo en memoria.
            login(request, user)

            # redireccionaremos al path con alias 'feed' que es para la url
            # 'posts/'
            return redirect("posts:feed")

        # En caso de dar false la autenticacion volveremos a renderizar el
        # login, pero enviando la variable 'error'.
        return render(
            request,
            "users/login.html",
            {"error": "Invalid username and password"},
        )

    return render(request, "users/login.html")


# Creamos la funcion logout_view, y lo decoramos con
# login_required, asi solo se ejecutara si existe una sesión.
@login_required
def logout_view(request):
    """
    logout view
    """

    # Ejecutamos logout, el cual borrara los tokens del navegador.
    logout(request)
    return redirect("users:login")  # Redirigimos a path de login.


def signup(request):
    """
    signup view
    """

    # Al recibir el metodo POST.
    if request.method == "POST":
        # Le enviamos los datos de request a nuestro formulario
        form = SignupForm(request.POST)

        # En caso de ser valido guarda las instancias
        # y nos redirige al login.
        if form.is_valid():
            form.save()
            return redirect("users:login")
    else:
        form = SignupForm()

    return render(
        request=request,
        template_name="users/signup.html",
        context={"form": form},
    )
