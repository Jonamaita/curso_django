"""
User Views
"""
# Importamos authenticate, login, logout
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Redirect nos ayudara a redireccionarnos a otro path
from django.shortcuts import redirect, render

# Forms
# Importamos el ProfileForm que creamos anteriormente
from users.forms import ProfileForm, SignupForm


@login_required
def update_profile(request):
    """
    Update a user's profile view
    """
    # Crearemos una variable que guardara el profile
    # que esta realizando el request.
    profile = request.user.profile

    # Si el request es de tipo 'POST'
    if request.method == 'POST':

        # Crearemos una instancia de ProfileForm
        # con los datos que recibimos a traves de request
        form = ProfileForm(request.POST, request.FILES)

        # Si la instacia se crea sin problemas.
        if form.is_valid():

            # Guardaremos los datos recibidos en base de datos.
            data = form.cleaned_data

            profile.website = data['website']
            profile.phone_number = data['phone_number']
            profile.biography = data['biography']
            if data["picture"]:
                profile.picture = data["picture"]
            profile.save()

            # Y redireccionaremos a la pagina update_profile
            # para reflejar los cambios.
            return redirect('update_profile')
    else:
        form = ProfileForm()

    return render(
        request=request,
        template_name='users/update_profile.html',

        # Enviaremos al template los datos del usuario.
        context={
            'profile': profile,
            'user': request.user,
            'form': form,
        }
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
    if request.method == 'POST':
        # Le enviamos los datos de request a nuestro formulario
        form = SignupForm(request.POST)

        # En caso de ser valido guarda las instancias
        # y nos redirige al login.
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()

    return render(
        request=request,
        template_name='users/signup.html',
        context={
            'form': form
        }
    )
