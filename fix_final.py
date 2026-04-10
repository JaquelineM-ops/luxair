content = open("AEROLINEA/templates/luxair/buscar_vuelos.html", encoding="utf-8").read()

old = """<div class="precio-opcion" onclick="event.stopPropagation(); window.location='/vuelos/seleccionar/{{ vuelo.id }}/?clase=economica'">
  <div class="precio-clase">EconÃ³mica</div>
  <div class="precio-monto">${{ vuelo.precio_economica|floatformat:0 }}</div>
</div>
<div class="precio-opcion" onclick="event.stopPropagation(); window.location='/vuelos/seleccionar/{{ vuelo.id }}/?clase=ejecutiva'">
  <div class="precio-clase">Ejecutiva</div>
  <div class="precio-monto">${{ vuelo.precio_ejecutiva|floatformat:0 }}</div>
</div>
<div class="precio-opcion" onclick="event.stopPropagation(); window.location='/vuelos/seleccionar/{{ vuelo.id }}/?clase=primera_clase'">
  <div class="precio-clase">1Âª Clase</div>
  <div class="precio-monto">${{ vuelo.precio_primera_clase|floatformat:0 }}</div>
</div>"""

new = """<div class="precio-opcion" onclick="event.stopPropagation(); seleccionarIda({{ vuelo.id }}, this.closest('.vuelo-card'))">
  <div class="precio-clase">Economica</div>
  <div class="precio-monto">${{ vuelo.precio_economica|floatformat:0 }}</div>
</div>
<div class="precio-opcion" onclick="event.stopPropagation(); seleccionarIda({{ vuelo.id }}, this.closest('.vuelo-card'))">
  <div class="precio-clase">Ejecutiva</div>
  <div class="precio-monto">${{ vuelo.precio_ejecutiva|floatformat:0 }}</div>
</div>
<div class="precio-opcion" onclick="event.stopPropagation(); seleccionarIda({{ vuelo.id }}, this.closest('.vuelo-card'))">
  <div class="precio-clase">1a Clase</div>
  <div class="precio-monto">${{ vuelo.precio_primera_clase|floatformat:0 }}</div>
</div>"""

result = content.replace(old, new)
if result == content:
    print("NO se encontro el texto a reemplazar")
else:
    open("AEROLINEA/templates/luxair/buscar_vuelos.html", "w", encoding="utf-8").write(result)
    print("Listo!")
