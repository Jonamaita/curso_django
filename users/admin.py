"""
User admin classes.
"""

from django.contrib import admin

from users.models import Profile

#Por convencion la clase que creemos debe terminar en Admin.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Profile admin.
    """
    # Con list_display nombramos los campos que queremos visualizar.
    list_display = ("pk", "user", "phone_number", "website", "picture")

    # list_display_links establece como links los campos nombrados.
    list_display_links = ("pk", "user")

    # list_editable nos permite editar el campo desde la lista del modelo en
    # vez de ingresar al detalle del registro.
    list_editable = ("phone_number", "picture")

    # Para crear un buscador hacemos uso de search_fields. Los campos que se
    # ingresan seran los que el buscador recorrera para realizar las busquedas.
    search_fields = (
        "user__email", # Se coloca doble underscore cuando es una relación.
        "user__username",
        "user__first_name",
        "user__last_name",
        "phone_number",
    )

    # Podemos crear un filtro para nuestro dashboard del modelo, para ello
    # usamos list_filter, y definimos los campos con los que trabajara.
    list_filter = (
        "user__is_active", # Se coloca doble underscore cuando es una relación.
        "user__is_staff",
        "created",
        "modified",
    )
