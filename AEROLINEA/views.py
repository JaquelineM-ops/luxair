from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, date
from django.views.decorators.http import require_POST
import json

from .models import (
    Usuario, Aeropuerto, Vuelo, Reservacion,
    Pasajero, Pago, Boleto, ReservacionGrupal, SolicitudGrupal
)
from .forms import (
    RegistroForm, LoginForm, BusquedaVueloForm,
    PasajeroForm, PagoForm, ReservacionGrupalForm
)


# ════════════════════════════════════════════════════════════
#  PÁGINAS PÚBLICAS
# ════════════════════════════════════════════════════════════

def inicio(request):
    """Página principal de LUX AIR"""
    destinos_populares = Aeropuerto.objects.all()[:6]
    context = {
        'destinos': destinos_populares,
        'aeropuertos': Aeropuerto.objects.all(),
    }
    return render(request, 'luxair/inicio.html', context)


def registro(request):
    """Registro de nuevo cliente"""
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, f'¡Bienvenida a LUX AIR, {usuario.first_name}! ✨')
            return redirect('inicio')
    else:
        form = RegistroForm()
    return render(request, 'luxair/registro.html', {'form': form})


def login_view(request):
    """Inicio de sesión"""
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            usuario = authenticate(request, username=username, password=password)
            if usuario:
                login(request, usuario)
                next_url = request.GET.get('next', 'inicio')
                return redirect(next_url)
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'luxair/login.html', {'form': form})




# ════════════════════════════════════════════════════════════
#  BÚSQUEDA Y SELECCIÓN DE VUELOS
# ════════════════════════════════════════════════════════════

def buscar_vuelos(request):
    """Búsqueda de vuelos disponibles"""
    vuelos_ida = []
    vuelos_regreso = []
    form = BusquedaVueloForm(request.GET or None)
    es_grupal = False

    if form.is_valid():
        origen = form.cleaned_data['origen']
        destino = form.cleaned_data['destino']
        fecha_salida = form.cleaned_data['fecha_salida']
        fecha_regreso = form.cleaned_data.get('fecha_regreso')
        num_pasajeros = form.cleaned_data['num_pasajeros']
        tipo_viaje = form.cleaned_data['tipo_viaje']

        if num_pasajeros > 8:
            es_grupal = True
            request.session['busqueda_grupal'] = {
                'origen_id': origen.id,
                'destino_id': destino.id,
                'fecha_salida': str(fecha_salida),
                'num_pasajeros': num_pasajeros,
            }
        else:
            vuelos_ida = Vuelo.objects.filter(
                origen=origen,
                destino=destino,
                fecha_salida__date=fecha_salida,
                estado='programado'
            ).order_by('fecha_salida')

            if tipo_viaje == 'redondo' and fecha_regreso:
                vuelos_regreso = Vuelo.objects.filter(
                    origen=destino,
                    destino=origen,
                    fecha_salida__date=fecha_regreso,
                    estado='programado'
                ).order_by('fecha_salida')

            # Guardar búsqueda en sesión
            request.session['busqueda'] = {
                'origen_id': origen.id,
                'destino_id': destino.id,
                'fecha_salida': str(fecha_salida),
                'fecha_regreso': str(fecha_regreso) if fecha_regreso else None,
                'num_pasajeros': num_pasajeros,
                'tipo_viaje': tipo_viaje,
            }

    context = {
        'form': form,
        'vuelos_ida': vuelos_ida,
        'vuelos_regreso': vuelos_regreso,
        'es_grupal': es_grupal,
        'aeropuertos': Aeropuerto.objects.all(),
    }
    return render(request, 'luxair/buscar_vuelos.html', context)


@login_required
def seleccionar_vuelo(request, vuelo_ida_id):
    """Seleccionar clase y vuelo de regreso"""
    vuelo_ida = get_object_or_404(Vuelo, id=vuelo_ida_id)
    busqueda = request.session.get('busqueda', {})
    vuelo_regreso = None

    if busqueda.get('tipo_viaje') == 'redondo' and request.GET.get('vuelo_regreso_id'):
        vuelo_regreso = get_object_or_404(Vuelo, id=request.GET.get('vuelo_regreso_id'))

    if request.method == 'POST':
        clase = request.POST.get('clase')
        vuelo_regreso_id = request.POST.get('vuelo_regreso_id')
        request.session['seleccion'] = {
            'vuelo_ida_id': vuelo_ida_id,
            'vuelo_regreso_id': vuelo_regreso_id,
            'clase': clase,
        }
        return redirect('datos_pasajeros')

    context = {
        'vuelo_ida': vuelo_ida,
        'vuelo_regreso': vuelo_regreso,
        'busqueda': busqueda,
        'precios': {
            'economica': vuelo_ida.precio_economica,
            'ejecutiva': vuelo_ida.precio_ejecutiva,
            'primera_clase': vuelo_ida.precio_primera_clase,
        }
    }
    return render(request, 'luxair/seleccionar_vuelo.html', context)


# ════════════════════════════════════════════════════════════
#  PROCESO DE RESERVACIÓN
# ════════════════════════════════════════════════════════════

@login_required
def datos_pasajeros(request):
    """Captura datos de pasajeros"""
    seleccion = request.session.get('seleccion', {})
    busqueda = request.session.get('busqueda', {})
    if not seleccion:
        return redirect('buscar_vuelos')

    num_pasajeros = busqueda.get('num_pasajeros', 1)
    vuelo_ida = get_object_or_404(Vuelo, id=seleccion['vuelo_ida_id'])

    if request.method == 'POST':
        pasajeros_data = []
        valido = True
        for i in range(num_pasajeros):
            form = PasajeroForm(request.POST, prefix=f'p{i}')
            if form.is_valid():
                pasajeros_data.append(form.cleaned_data)
            else:
                valido = False

        tua_opcion = request.POST.get('tua_opcion', 'ahora')
        equipaje_extra = int(request.POST.get('equipaje_extra', 0))

        if valido:
            request.session['pasajeros_data'] = pasajeros_data
            request.session['servicios'] = {
                'tua_opcion': tua_opcion,
                'equipaje_extra': equipaje_extra,
            }
            # Serializar fechas
            for p in request.session['pasajeros_data']:
                if 'fecha_nacimiento' in p and hasattr(p['fecha_nacimiento'], 'isoformat'):
                    p['fecha_nacimiento'] = p['fecha_nacimiento'].isoformat()
            return redirect('resumen_compra')

    forms_pasajeros = [PasajeroForm(prefix=f'p{i}') for i in range(num_pasajeros)]
    context = {
        'forms_pasajeros': forms_pasajeros,
        'vuelo_ida': vuelo_ida,
        'seleccion': seleccion,
        'num_pasajeros': num_pasajeros,
        'tua_precio': vuelo_ida.tua,
    }
    return render(request, 'luxair/datos_pasajeros.html', context)


@login_required
def resumen_compra(request):
    """Resumen y detalles de la compra"""
    seleccion = request.session.get('seleccion', {})
    busqueda = request.session.get('busqueda', {})
    pasajeros_data = request.session.get('pasajeros_data', [])
    servicios = request.session.get('servicios', {})

    if not seleccion or not pasajeros_data:
        return redirect('buscar_vuelos')

    vuelo_ida = get_object_or_404(Vuelo, id=seleccion['vuelo_ida_id'])
    vuelo_regreso = None
    if seleccion.get('vuelo_regreso_id'):
        vuelo_regreso = get_object_or_404(Vuelo, id=seleccion['vuelo_regreso_id'])

    clase = seleccion['clase']
    num_pasajeros = len(pasajeros_data)

    # Calcular precios
    precio_clase = getattr(vuelo_ida, f'precio_{clase}')
    subtotal = float(precio_clase) * num_pasajeros
    if vuelo_regreso:
        precio_regreso = getattr(vuelo_regreso, f'precio_{clase}')
        subtotal += float(precio_regreso) * num_pasajeros

    tua_total = 0
    if servicios.get('tua_opcion') == 'ahora':
        tua_total = float(vuelo_ida.tua) * num_pasajeros
        if vuelo_regreso:
            tua_total += float(vuelo_regreso.tua) * num_pasajeros

    equipaje_extra = servicios.get('equipaje_extra', 0)
    extras_total = equipaje_extra * 500 * num_pasajeros  # $500 por maleta extra

    total = subtotal + tua_total + extras_total

    context = {
        'vuelo_ida': vuelo_ida,
        'vuelo_regreso': vuelo_regreso,
        'pasajeros_data': pasajeros_data,
        'seleccion': seleccion,
        'servicios': servicios,
        'clase': clase,
        'num_pasajeros': num_pasajeros,
        'precio_clase': precio_clase,
        'subtotal': subtotal,
        'tua_total': tua_total,
        'extras_total': extras_total,
        'total': total,
        'equipaje_extra': equipaje_extra,
    }
    request.session['totales'] = {
        'subtotal': subtotal,
        'tua_total': tua_total,
        'extras_total': extras_total,
        'total': total,
    }
    return render(request, 'luxair/resumen_compra.html', context)


@login_required
def pago(request):
    """Proceso de pago"""
    seleccion = request.session.get('seleccion', {})
    totales = request.session.get('totales', {})
    if not seleccion or not totales:
        return redirect('buscar_vuelos')

    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            # Crear reservación
            vuelo_ida = get_object_or_404(Vuelo, id=seleccion['vuelo_ida_id'])
            pasajeros_data = request.session.get('pasajeros_data', [])
            servicios = request.session.get('servicios', {})
            busqueda = request.session.get('busqueda', {})

            reservacion = Reservacion.objects.create(
                usuario=request.user,
                vuelo_ida=vuelo_ida,
                clase=seleccion['clase'],
                tipo_viaje=busqueda.get('tipo_viaje', 'ida'),
                tua_opcion=servicios.get('tua_opcion', 'ahora'),
                equipaje_extra=servicios.get('equipaje_extra', 0),
                subtotal=totales['subtotal'],
                tua_total=totales['tua_total'],
                extras_total=totales['extras_total'],
                total=totales['total'],
                estado='confirmada',
            )

            if seleccion.get('vuelo_regreso_id'):
                reservacion.vuelo_regreso_id = seleccion['vuelo_regreso_id']
                reservacion.save()

            # Crear pasajeros y boletos
            asientos = ['1A','1B','1C','2A','2B','2C','3A','3B','3C','4A','4B','4C']
            for i, p_data in enumerate(pasajeros_data):
                pasajero = Pasajero.objects.create(
                    reservacion=reservacion,
                    nombre=p_data['nombre'],
                    apellido_paterno=p_data['apellido_paterno'],
                    apellido_materno=p_data.get('apellido_materno', ''),
                    fecha_nacimiento=p_data['fecha_nacimiento'],
                    tipo=p_data.get('tipo', 'adulto'),
                    nacionalidad=p_data.get('nacionalidad', 'Mexicana'),
                    necesidades_especiales=p_data.get('necesidades_especiales', ''),
                    asiento=asientos[i % len(asientos)],
                )
                Boleto.objects.create(
                    reservacion=reservacion,
                    pasajero=pasajero,
                    vuelo=vuelo_ida,
                    asiento=asientos[i % len(asientos)],
                    clase=seleccion['clase'],
                )
                if seleccion.get('vuelo_regreso_id'):
                    vuelo_regreso = get_object_or_404(Vuelo, id=seleccion['vuelo_regreso_id'])
                    Boleto.objects.create(
                        reservacion=reservacion,
                        pasajero=pasajero,
                        vuelo=vuelo_regreso,
                        asiento=asientos[i % len(asientos)],
                        clase=seleccion['clase'],
                    )

            # Crear pago
            Pago.objects.create(
                reservacion=reservacion,
                metodo=form.cleaned_data['metodo'],
                estado='aprobado',
                monto=totales['total'],
                ultimos_4=form.cleaned_data.get('ultimos_4', ''),
                nombre_titular=form.cleaned_data.get('nombre_titular', ''),
            )

            # Limpiar sesión
            for key in ['busqueda', 'seleccion', 'pasajeros_data', 'servicios', 'totales']:
                request.session.pop(key, None)

            messages.success(request, '¡Pago autorizado! Tu boleto LUX AIR está listo. ✈️')
            return redirect('confirmacion', codigo=str(reservacion.codigo))
    else:
        form = PagoForm()

    context = {
        'form': form,
        'totales': totales,
        'seleccion': seleccion,
    }
    return render(request, 'luxair/pago.html', context)
@login_required
def mi_cuenta(request):
    reservaciones = Reservacion.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    solicitudes_grupales = SolicitudGrupal.objects.filter(usuario=request.user).order_by('-fecha_solicitud')
    return render(request, 'luxair/mi_cuenta.html', {
        'reservaciones': reservaciones,
        'solicitudes_grupales': solicitudes_grupales,
    })

@login_required
def mis_boletos(request):
    boletos = Boleto.objects.filter(reservacion__usuario=request.user)
    return render(request, 'luxair/mis_boletos.html', {'boletos': boletos})

@login_required
def panel_admin(request):
    if request.user.rol not in ['admin', 'empleado']:
        return redirect('inicio')
    vuelos_hoy = Vuelo.objects.filter(fecha_salida__date=date.today())
    reservaciones_recientes = Reservacion.objects.order_by('-fecha_creacion')[:10]
    context = {
        'vuelos_hoy': vuelos_hoy,
        'reservaciones_recientes': reservaciones_recientes,
        'total_vuelos': Vuelo.objects.count(),
        'total_reservaciones': Reservacion.objects.filter(estado='confirmada').count(),
    }
    return render(request, 'luxair/admin/panel.html', context)

@login_required
def confirmacion(request, codigo):
    """Página de confirmación y boleto"""
    reservacion = get_object_or_404(Reservacion, codigo=codigo, usuario=request.user)
    boletos = Boleto.objects.filter(reservacion=reservacion)
    return render(request, 'luxair/confirmacion.html', {
        'reservacion': reservacion,
        'boletos': boletos,
    })


# ════════════════════════════════════════════════════════════
#  VUELO GRUPAL
# ════════════════════════════════════════════════════════════

@login_required
def vuelo_grupal(request):
    busqueda_grupal = request.session.get('busqueda_grupal', {})
    if request.method == 'POST':
        nombre   = request.POST.get('nombre_contacto', '').strip()
        email    = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        num_pas  = request.POST.get('num_pasajeros', '').strip()
        comentarios = request.POST.get('comentarios', '').strip()

        if nombre and email and telefono and num_pas:
            from .models import SolicitudGrupal
            SolicitudGrupal.objects.create(
                usuario=request.user if request.user.is_authenticated else None,
                nombre_contacto=nombre,
                email=email,
                telefono=telefono,
                num_pasajeros=int(num_pas),
                comentarios=comentarios,
            )
            messages.success(request, '¡Tu solicitud grupal fue enviada! Un agente LUX AIR te contactará pronto. 🌟')
            return redirect('inicio')
        else:
            return render(request, 'luxair/vuelo_grupal.html', {
                'error': 'Por favor completa todos los campos obligatorios.',
                'datos': request.POST,
                'busqueda': busqueda_grupal,
            })

    return render(request, 'luxair/vuelo_grupal.html', {'busqueda': busqueda_grupal})
# ════════════════════════════════════════════════════════════
#  API ENDPOINTS (AJAX)
# ════════════════════════════════════════════════════════════

def api_aeropuertos(request):
    """Autocompletado de aeropuertos"""
    q = request.GET.get('q', '')
    aeropuertos = Aeropuerto.objects.filter(
        Q(ciudad__icontains=q) | Q(codigo_iata__icontains=q) | Q(nombre__icontains=q)
    )[:10]
    data = [{'id': a.id, 'text': str(a), 'iata': a.codigo_iata, 'ciudad': a.ciudad} for a in aeropuertos]
    return JsonResponse({'results': data})

# check-in 

def checkin(request):
    ctx = {}
    if request.method == 'POST' and 'codigo' in request.POST:
        codigo   = request.POST.get('codigo','').strip().replace('LX-','').strip()
        apellido = request.POST.get('apellido','').strip()
        try:
            res = Reservacion.objects.get(
                usuario=request.user,
                usuario__last_name__iexact=apellido
            )
            ctx['reservacion'] = res
        except Reservacion.DoesNotExist:
            # Intentar por pasajero
            try:
                from .models import Pasajero
                pasajero = Pasajero.objects.get(
                    apellido_paterno__iexact=apellido,
                    reservacion__usuario=request.user
                )
                ctx['reservacion'] = pasajero.reservacion
            except:
                ctx['error'] = 'No encontramos esa reservación. Verifica el código y apellido.'
        except Exception:
            ctx['error'] = 'No encontramos esa reservación. Verifica el código y apellido.'

    if request.method == 'POST' and 'reservacion_id' in request.POST:
        res = get_object_or_404(Reservacion, id=request.POST['reservacion_id'])
        res.checkin_realizado = True
        res.save()
        ctx['reservacion'] = res
        ctx['checkin_ok'] = True

    return render(request, 'luxair/checkin.html', ctx)

@login_required
def pagar_grupal(request, reservacion_id):
    from .models import ReservacionGrupal
    reservacion = get_object_or_404(ReservacionGrupal, id=reservacion_id)

    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            reservacion.estado = 'confirmada'
            reservacion.save()
            # Marcar solicitud como atendida
            if reservacion.solicitud:
                reservacion.solicitud.atendida = True
                reservacion.solicitud.save()
            messages.success(request, '¡Pago realizado! Tu reservación grupal está confirmada. ✦')
            return redirect('mi_cuenta')
    else:
        form = PagoForm()

    return render(request, 'luxair/pago_grupal.html', {
        'form': form,
        'reservacion': reservacion,
    })

@login_required
def perfil(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.telefono = request.POST.get('telefono', '').strip()
        user.domicilio = request.POST.get('domicilio', '').strip()
        user.genero = request.POST.get('genero', 'O')
        user.fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
        user.save()
        messages.success(request, '¡Perfil actualizado correctamente! ✦')
        return redirect('perfil')
    return render(request, 'luxair/perfil.html', {'user': request.user})
    