"""
User Views
"""
# Importamos authenticate, login, logout
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Models
# Importamos los modelos de las instancias que crearemos
from django.contrib.auth.models import User
# Exceptions
# Importamos posible error al tratar de crear una instancia
# con valor único que ya existe
from django.db.utils import IntegrityError
# Redirect nos ayudara a redireccionarnos a otro path
from django.shortcuts import redirect, render

from users.models import Profile


def update_profile(request):
    """
    Update a user's profile view
    """
    return render(request, 'users/update_profile.html')


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
            return redirect("feed")

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
    return redirect("login")  # Redirigimos a path de login.


def signup(request):
    """
    signup view
    """
    # Al recibir el metodo POST.
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password_confirmation = request.POST["password_confirmation"]

        # Confirmamos que las constraseñas sean iguales.
        if password != password_confirmation:
            # En caso de error volvemos a renderizar signup, pero enviamos
            # el error
            return render(
                request,
                "users/signup.html",
                {"error": "Passwords does not match"},
            )

        try:
            # Creamos una instancia de User
            user = User.objects.create_user(
                username=username, password=password
            )
        except IntegrityError:
            # En caso que username (nuestro valor unico) ya exista renderizara
            # nuevamente signup pero enviando el error.
            return render(
                request,
                "users/signup.html",
                {"error": "Username is already exist"},
            )

        # Ya creada la instancia le pasamos los siguientes valores.
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.email = request.POST["email"]
        # Lo guardamos en nuestra base de datos.
        user.save()

        # Creamos nuestra instacia de Profile a traves de user.
        profile = Profile(user=user)
        # Lo guardamos en la base de datos.
        profile.save()

        # Nos redirigimos a login para iniciar sesion con el nuevo usuario.
        return redirect("login")

    return render(request, "users/signup.html")
