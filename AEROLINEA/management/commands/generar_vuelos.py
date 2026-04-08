from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from AEROLINEA.models import Vuelo, Aeropuerto, Avion
import random

class Command(BaseCommand):
    help = 'Genera 2 vuelos diarios para todas las rutas hasta fin de año'

    def handle(self, *args, **kwargs):
        aeropuertos = list(Aeropuerto.objects.all())
        aviones = list(Avion.objects.filter(activo=True))

        if not aviones:
            self.stdout.write(self.style.ERROR('No hay aviones disponibles'))
            return

        hoy = datetime.today().date()
        fin_anio = datetime(2026, 12, 31).date()
        contador = 0
        numero_vuelo = Vuelo.objects.count() * 10 + 100

        horarios = [
            ('06:00', '08:30'),
            ('14:00', '16:30'),
        ]

        for origen in aeropuertos:
            for destino in aeropuertos:
                if origen == destino:
                    continue
                fecha = hoy
                while fecha <= fin_anio:
                    for salida, llegada in horarios:
                        numero_vuelo += 1
                        num_str = f"{numero_vuelo:04d}"
                        if not Vuelo.objects.filter(numero_vuelo=num_str).exists():
                            avion = random.choice(aviones)
                            fecha_salida = timezone.make_aware(
                                datetime.combine(fecha, datetime.strptime(salida, '%H:%M').time())
                            )
                            fecha_llegada = timezone.make_aware(
                                datetime.combine(fecha, datetime.strptime(llegada, '%H:%M').time())
                            )
                            Vuelo.objects.create(
                                numero_vuelo=num_str,
                                origen=origen,
                                destino=destino,
                                avion=avion,
                                fecha_salida=fecha_salida,
                                fecha_llegada=fecha_llegada,
                                precio_economica=random.choice([1299, 1499, 1799, 2099]),
                                precio_ejecutiva=random.choice([4899, 5499, 6299]),
                                precio_primera_clase=random.choice([12500, 14000, 16000]),
                                tua=310,
                                estado='programado',
                            )
                            contador += 1
                    fecha += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS(f'✓ {contador} vuelos generados exitosamente'))
