content = open("AEROLINEA/templates/luxair/buscar_vuelos.html", encoding="utf-8").read()

old = """        <div class="precio-opcion" onclick="event.stopPropagation(); window.location='/vuelos/seleccionar/{{ vuelo.id }}/?clase=economica'">
  <div class="precio-clase">Econ\u00c3\u00b3mica</div>
  <div class="precio-monto">${{ vuelo.precio_economica|floatformat:0 }}</div>
</div>
<div class="precio-opcion" onclick="event.stopPropagation(); window.location='/vuelos/seleccionar/{{ vuelo.id }}/?clase=ejecutiva'">
  <div class="precio-clase">Ejecutiva</div>
  <div class="precio-monto">${{ vuelo.precio_ejecutiva|floatformat:0 }}</div>
</div>
<div class="precio-opcion" onclick="event.stopPropagation(); window.location='/vuelos/seleccionar/{{ vuelo.id }}/?clase=primera_clase'">
  <div class="precio-clase">1\u00c2\u00aaClase</div>
  <div class="precio-monto">${{ vuelo.precio_primera_clase|floatformat:0 }}</div>
</div>"""

print("Buscando precio-opcion...")
idx = content.find("window.location='/vuelos/seleccionar/{{ vuelo.id }}/?clase=economica'")
print(f"Encontrado en indice: {idx}")
if idx > 0:
    print(repr(content[idx-50:idx+200]))
