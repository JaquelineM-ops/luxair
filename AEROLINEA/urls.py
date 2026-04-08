from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Públicas
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Búsqueda de vuelos
    path('vuelos/', views.buscar_vuelos, name='buscar_vuelos'),
    path('vuelos/seleccionar/<int:vuelo_ida_id>/', views.seleccionar_vuelo, name='seleccionar_vuelo'),
    path('vuelos/grupal/', views.vuelo_grupal, name='vuelo_grupal'),

    # Proceso de compra
    path('reservar/pasajeros/', views.datos_pasajeros, name='datos_pasajeros'),
    path('reservar/resumen/', views.resumen_compra, name='resumen_compra'),
    path('reservar/pago/', views.pago, name='pago'),
    path('reservar/confirmacion/<uuid:codigo>/', views.confirmacion, name='confirmacion'),

    # Cuenta del cliente
    path('mi-cuenta/', views.mi_cuenta, name='mi_cuenta'),
    path('mis-boletos/', views.mis_boletos, name='mis_boletos'),

    # Panel admin/empleado
    path('panel/', views.panel_admin, name='panel_admin'),

    # API
    path('api/aeropuertos/', views.api_aeropuertos, name='api_aeropuertos'),

    #Check-in cliente
    path('checkin/', views.checkin, name='checkin'),

    path('reservar/grupal/<int:reservacion_id>/pagar/', views.pagar_grupal, name='pagar_grupal'),

    path('mi-cuenta/perfil/', views.perfil, name='perfil'),
]


