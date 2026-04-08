from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


# ─── USUARIO PERSONALIZADO ───────────────────────────────────────────────────
class Usuario(AbstractUser):
    ROL_CHOICES = [('cliente', 'Cliente'), ('admin', 'Administrador'), ('empleado', 'Empleado')]
    GENERO_CHOICES = [('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='cliente')
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, default='O')
    telefono = models.CharField(max_length=20, blank=True)
    domicilio = models.CharField(max_length=255, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.rol})"

# ─── AEROPUERTO ───────────────────────────────────────────────────────────────
class Aeropuerto(models.Model):
    codigo_iata = models.CharField(max_length=3, unique=True)
    nombre = models.CharField(max_length=150)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='aeropuertos/', null=True, blank=True)

    def __str__(self):
        return f"{self.codigo_iata} — {self.ciudad}, {self.pais}"
    
class ImagenAeropuerto(models.Model):
    aeropuerto = models.ForeignKey(Aeropuerto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='aeropuertos/')
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"Imagen {self.orden} — {self.aeropuerto.ciudad}"


# ─── AVIÓN ────────────────────────────────────────────────────────────────────
class Avion(models.Model):
    modelo = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)
    capacidad_economica = models.PositiveIntegerField(default=120)
    capacidad_ejecutiva = models.PositiveIntegerField(default=30)
    capacidad_primera_clase = models.PositiveIntegerField(default=10)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.modelo} ({self.matricula})"


# ─── EMPLEADO ─────────────────────────────────────────────────────────────────
class Empleado(models.Model):
    PUESTO_CHOICES = [
        ('piloto', 'Piloto'),
        ('copiloto', 'Copiloto'),
        ('auxiliar', 'Auxiliar de vuelo'),
        ('tecnico', 'Técnico de tierra'),
        ('mostrador', 'Agente de mostrador'),
    ]
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='empleado')
    numero_empleado = models.CharField(max_length=20, unique=True)
    puesto = models.CharField(max_length=30, choices=PUESTO_CHOICES)
    fecha_ingreso = models.DateField()
    licencia = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.usuario.get_full_name()} — {self.puesto}"


# ─── VUELO ────────────────────────────────────────────────────────────────────
class Vuelo(models.Model):
    ESTADO_CHOICES = [
        ('programado', 'Programado'),
        ('embarque', 'En embarque'),
        ('en_vuelo', 'En vuelo'),
        ('aterrizado', 'Aterrizado'),
        ('cancelado', 'Cancelado'),
        ('retrasado', 'Retrasado'),
    ]
    numero_vuelo = models.CharField(max_length=10, unique=True)
    origen = models.ForeignKey(Aeropuerto, on_delete=models.PROTECT, related_name='vuelos_salida')
    destino = models.ForeignKey(Aeropuerto, on_delete=models.PROTECT, related_name='vuelos_llegada')
    avion = models.ForeignKey(Avion, on_delete=models.PROTECT, related_name='vuelos')
    fecha_salida = models.DateTimeField()
    fecha_llegada = models.DateTimeField()
    precio_economica = models.DecimalField(max_digits=10, decimal_places=2)
    precio_ejecutiva = models.DecimalField(max_digits=10, decimal_places=2)
    precio_primera_clase = models.DecimalField(max_digits=10, decimal_places=2)
    tua = models.DecimalField(max_digits=8, decimal_places=2, default=310.00)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='programado')
    tripulacion = models.ManyToManyField(Empleado, blank=True, related_name='vuelos_asignados')

    def asientos_disponibles(self, clase):
        ocupados = self.reservaciones.filter(clase=clase, estado__in=['confirmada', 'pendiente']).count()
        if clase == 'economica':
            return self.avion.capacidad_economica - ocupados
        elif clase == 'ejecutiva':
            return self.avion.capacidad_ejecutiva - ocupados
        elif clase == 'primera_clase':
            return self.avion.capacidad_primera_clase - ocupados
        return 0

    def __str__(self):
        return f"LX{self.numero_vuelo} | {self.origen.codigo_iata} → {self.destino.codigo_iata} | {self.fecha_salida.strftime('%d/%m/%Y %H:%M')}"


# ─── PASAJERO ─────────────────────────────────────────────────────────────────
class Pasajero(models.Model):
    TIPO_CHOICES = [
        ('adulto', 'Adulto'),
        ('menor', 'Menor de edad'),
        ('tercera_edad', 'Tercera edad'),
        ('discapacidad', 'Persona con discapacidad'),
    ]
    reservacion = models.ForeignKey('Reservacion', on_delete=models.CASCADE, related_name='pasajeros')
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100, blank=True)
    fecha_nacimiento = models.DateField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='adulto')
    numero_pasaporte = models.CharField(max_length=20, blank=True)
    nacionalidad = models.CharField(max_length=60, default='Mexicana')
    asiento = models.CharField(max_length=5, blank=True)
    necesidades_especiales = models.TextField(blank=True)
    checkin_realizado = models.BooleanField(default=False)

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}".strip()

    def __str__(self):
        return self.nombre_completo()


# ─── RESERVACIÓN ──────────────────────────────────────────────────────────────
class Reservacion(models.Model):
    CLASE_CHOICES = [
        ('economica', 'Económica'),
        ('ejecutiva', 'Ejecutiva'),
        ('primera_clase', 'Primera Clase'),
    ]
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente de pago'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('check_in', 'Check-in realizado'),
        ('abordado', 'Abordado'),
    ]
    TIPO_VIAJE_CHOICES = [
        ('ida', 'Solo ida'),
        ('redondo', 'Vuelo redondo'),
        ('grupal', 'Vuelo grupal'),
    ]
    TUA_PAGO_CHOICES = [
        ('ahora', 'Pagar TUA ahora'),
        ('despues', 'Pagar TUA después (check-in)'),
    ]

    codigo = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='reservaciones')
    vuelo_ida = models.ForeignKey(Vuelo, on_delete=models.PROTECT, related_name='reservaciones')
    vuelo_regreso = models.ForeignKey(Vuelo, on_delete=models.PROTECT, related_name='reservaciones_regreso', null=True, blank=True)
    clase = models.CharField(max_length=20, choices=CLASE_CHOICES)
    tipo_viaje = models.CharField(max_length=10, choices=TIPO_VIAJE_CHOICES, default='ida')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    tua_opcion = models.CharField(max_length=10, choices=TUA_PAGO_CHOICES, default='ahora')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    # Servicios extra
    equipaje_extra = models.PositiveIntegerField(default=0, help_text="Número de maletas extra")
    asientos_seleccionados = models.BooleanField(default=False)

    # Totales
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tua_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    extras_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def numero_pasajeros(self):
        return self.pasajeros.count()

    def __str__(self):
        return f"Reserv. {str(self.codigo)[:8].upper()} — {self.usuario}"


# ─── PAGO ─────────────────────────────────────────────────────────────────────
class Pago(models.Model):
    METODO_CHOICES = [
        ('tarjeta', 'Tarjeta de crédito/débito'),
        ('paypal', 'PayPal'),
        ('mostrador', 'En mostrador'),
    ]
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
        ('reembolsado', 'Reembolsado'),
    ]
    reservacion = models.OneToOneField(Reservacion, on_delete=models.CASCADE, related_name='pago')
    metodo = models.CharField(max_length=20, choices=METODO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    referencia = models.CharField(max_length=100, blank=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    # Datos tarjeta (solo últimos 4 dígitos por seguridad)
    ultimos_4 = models.CharField(max_length=4, blank=True)
    nombre_titular = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Pago {self.estado} — {self.reservacion.codigo}"


# ─── BOLETO ───────────────────────────────────────────────────────────────────
class Boleto(models.Model):
    codigo_boleto = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    reservacion = models.ForeignKey(Reservacion, on_delete=models.CASCADE, related_name='boletos')
    pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE, related_name='boleto')
    vuelo = models.ForeignKey(Vuelo, on_delete=models.CASCADE, related_name='boletos')
    asiento = models.CharField(max_length=5)
    clase = models.CharField(max_length=20)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    check_in_realizado = models.BooleanField(default=False)
    abordado = models.BooleanField(default=False)

    def __str__(self):
        return f"Boleto {str(self.codigo_boleto)[:8].upper()} — {self.pasajero} | {self.vuelo}"


# ─── RESERVACIÓN GRUPAL ───────────────────────────────────────────────────────
class ReservacionGrupal(models.Model):
    ESTADO_CHOICES = [
        ('cotizacion', 'En cotización'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    
    nombre_grupo = models.CharField(max_length=150)
    organizador = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    numero_pasajeros = models.PositiveIntegerField(validators=[MinValueValidator(9)])
    descuento_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=15.00)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='cotizacion')
    notas = models.TextField(blank=True)
    solicitud = models.ForeignKey(

        'SolicitudGrupal',
         on_delete=models.SET_NULL,
         null=True,
         blank=True,
         related_name='reservacion_grupal'
)
    precio_cotizado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Grupo '{self.nombre_grupo}' — {self.numero_pasajeros} pasajeros"

    #SOLICITUD GRUPAL

    
class SolicitudGrupal(models.Model):
    usuario         = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_contacto = models.CharField(max_length=100)
    email           = models.CharField(max_length=100)
    telefono        = models.CharField(max_length=20)
    num_pasajeros   = models.IntegerField()
    comentarios     = models.TextField(blank=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    atendida        = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre_contacto} — {self.num_pasajeros} pax"