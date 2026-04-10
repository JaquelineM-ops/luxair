content = open('AEROLINEA/templates/luxair/buscar_vuelos.html', encoding='utf-8').read()

old = '  <div class="vuelo-card" onclick="window.location=\'/vuelos/seleccionar/{{ vuelo.id }}/\'">'
new = '  <div class="vuelo-card vuelo-ida-href" data-id="{{ vuelo.id }}" onclick="window.location=\'/vuelos/seleccionar/{{ vuelo.id }}/\'">'

content = content.replace(old, new)
open('AEROLINEA/templates/luxair/buscar_vuelos.html', 'w', encoding='utf-8').write(content)
print('Listo!')
