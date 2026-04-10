content = open('AEROLINEA/templates/luxair/buscar_vuelos.html', encoding='utf-8').read()

old = '''function seleccionarIda(vuelo_id, card) {
  // Resaltar ida seleccionada
  document.querySelectorAll('.vuelo-card').forEach(c => c.style.borderColor = '');
  card.style.borderColor = 'var(--gold)';
  idaSeleccionada = vuelo_id;
  // Si es solo ida, ir directo
  if(document.getElementById('tipo_viaje_input').value !== 'redondo') {
    window.location = '/vuelos/seleccionar/' + vuelo_id + '/';
    return;
  }
  // Si es redondo, mostrar mensaje para seleccionar regreso
  var msg = document.getElementById('msg-selecciona-regreso');
  if(msg) msg.style.display = 'block';
  document.getElementById('btn-continuar-redondo').style.display = 'none';
}'''

new = '''function seleccionarIda(vuelo_id, card) {
  document.querySelectorAll('.vuelo-card').forEach(c => c.style.borderColor = '');
  card.style.borderColor = 'var(--gold)';
  idaSeleccionada = vuelo_id;
  var tieneRegreso = document.getElementById('msg-selecciona-regreso');
  if(tieneRegreso) {
    tieneRegreso.style.display = 'block';
    tieneRegreso.scrollIntoView({behavior:'smooth'});
    document.getElementById('btn-continuar-redondo').style.display = 'none';
  } else {
    window.location = '/vuelos/seleccionar/' + vuelo_id + '/';
  }
}'''

content = content.replace(old, new)
open('AEROLINEA/templates/luxair/buscar_vuelos.html', 'w', encoding='utf-8').write(content)
print('Listo!')
