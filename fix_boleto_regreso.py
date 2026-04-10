content = open("AEROLINEA/views.py", encoding="utf-8").read()

old = """                Boleto.objects.create(
                    reservacion=reservacion,
                    pasajero=pasajero,
                    vuelo=vuelo_ida,
                    asiento=asientos[i % len(asientos)],
                    clase=seleccion['clase'],
                )"""

new = """                Boleto.objects.create(
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
                    )"""

result = content.replace(old, new)
if result == content:
    print("NO encontrado")
else:
    open("AEROLINEA/views.py", "w", encoding="utf-8").write(result)
    print("Listo!")
