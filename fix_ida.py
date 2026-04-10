content = open('AEROLINEA/templates/luxair/buscar_vuelos.html', encoding='utf-8').read()

old = '  <div class="vuelo-card" onclick="window.location=\'/vuelos/seleccionar/{{ vuelo.id }}/\'">'
new = '  <div class="vuelo-card" onclick="seleccionarIda({{ vuelo.id }}, this)">'
content = content.replace(old, new)

old2 = "      <a href=\"{% url 'seleccionar_vuelo' vuelo.id %}\" class=\"vuelo-seleccionar\">\n        Seleccionar \xe2\x80\xba\n      </a>"
new2 = '      <button class="vuelo-seleccionar" onclick="event.stopPropagation(); seleccionarIda({{ vuelo.id }}, this.closest(\'vuelo-card\'))">Seleccionar ›</button>'
content = content.replace(old2, new2)

open('AEROLINEA/templates/luxair/buscar_vuelos.html', 'w', encoding='utf-8').write(content)
print(f'Reemplazos hechos')
