from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Aeropuerto, Avion, Empleado, Vuelo, Pasajero, Reservacion, Pago, Boleto, ReservacionGrupal

admin.site.site_header = "✈️ LUX AIR — Panel de Administración"
admin.site.site_title = "LUX AIR Admin"
admin.site.index_title = "Bienvenido al panel de control"


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_active')
    list_filter = ('rol', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('LUX AIR', {'fields': ('rol','genero','telefono','domicilio', 'fecha_nacimiento', 'foto_perfil')}),
    )


from .models import ImagenAeropuerto

class ImagenAeropuertoInline(admin.TabularInline):
    model = ImagenAeropuerto
    extra = 3

@admin.register(Aeropuerto)
class AeropuertoAdmin(admin.ModelAdmin):
    list_display = ('codigo_iata', 'nombre', 'ciudad', 'pais')
    search_fields = ('codigo_iata', 'ciudad', 'nombre')
    inlines = [ImagenAeropuertoInline]


@admin.register(Avion)
class AvionAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'modelo', 'capacidad_economica', 'capacidad_ejecutiva', 'capacidad_primera_clase', 'activo')
    list_filter = ('activo',)


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('numero_empleado', 'usuario', 'puesto', 'fecha_ingreso')
    list_filter = ('puesto',)
    search_fields = ('numero_empleado', 'usuario__first_name', 'usuario__last_name')


class PasajeroInline(admin.TabularInline):
    model = Pasajero
    extra = 0


class BoletoInline(admin.TabularInline):
    model = Boleto
    extra = 0
    readonly_fields = ('codigo_boleto', 'fecha_emision')


@admin.register(Vuelo)
class VueloAdmin(admin.ModelAdmin):
    list_display = ('numero_vuelo', 'origen', 'destino', 'fecha_salida', 'fecha_llegada', 'estado', 'avion')
    list_filter = ('estado', 'origen', 'destino')
    search_fields = ('numero_vuelo',)
    filter_horizontal = ('tripulacion',)
    date_hierarchy = 'fecha_salida'


@admin.register(Reservacion)
class ReservacionAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'usuario', 'vuelo_ida', 'clase', 'tipo_viaje', 'estado', 'total', 'fecha_creacion')
    list_filter = ('estado', 'clase', 'tipo_viaje')
    search_fields = ('codigo', 'usuario__username', 'usuario__email')
    readonly_fields = ('codigo', 'fecha_creacion', 'fecha_actualizacion')
    inlines = [PasajeroInline, BoletoInline]
    date_hierarchy = 'fecha_creacion'


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('reservacion', 'metodo', 'estado', 'monto', 'fecha_pago')
    list_filter = ('metodo', 'estado')
    readonly_fields = ('fecha_pago',)


@admin.register(Boleto)
class BoletoAdmin(admin.ModelAdmin):
    list_display = ('codigo_boleto', 'pasajero', 'vuelo', 'asiento', 'clase', 'check_in_realizado', 'abordado')
    list_filter = ('clase', 'check_in_realizado', 'abordado')
    search_fields = ('codigo_boleto', 'pasajero__nombre')
    readonly_fields = ('codigo_boleto', 'fecha_emision')


@admin.register(ReservacionGrupal)
class ReservacionGrupalAdmin(admin.ModelAdmin):
    list_display = ('nombre_grupo', 'organizador', 'numero_pasajeros', 'descuento_porcentaje', 'estado')
    list_filter = ('estado',)

from .models import SolicitudGrupal

from django.utils.html import format_html
from django.urls import reverse

@admin.register(SolicitudGrupal)
class SolicitudGrupalAdmin(admin.ModelAdmin):
    list_display  = ['nombre_contacto', 'email', 'telefono', 'num_pasajeros', 'fecha_solicitud', 'atendida', 'boton_reservacion']
    list_filter   = ['atendida']
    list_editable = ['atendida']
    actions       = ['marcar_atendida']

    def boton_reservacion(self, obj):
        if not obj.atendida:
            url = reverse('admin:AEROLINEA_reservaciongrupal_add')
            return format_html(
                '<a href="{}?nombre_grupo={}&numero_pasajeros={}" '
                'style="background:#8B5A00;color:#fff;padding:.3rem .75rem;'
                'border-radius:6px;text-decoration:none;font-size:.8rem">'
                '✦ Crear Reservación</a>',
                url,
                obj.nombre_contacto,
                obj.num_pasajeros,
            )
        return '✔ Atendida'
    boton_reservacion.short_description = 'Acción'

    def marcar_atendida(self, request, queryset):
        queryset.update(atendida=True)
        self.message_user(request, f'{queryset.count()} solicitud(es) marcadas como atendidas.')
    marcar_atendida.short_description = '✔ Marcar como atendida'