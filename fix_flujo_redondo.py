content = open('AEROLINEA/templates/luxair/buscar_vuelos.html', encoding='utf-8').read()

old = '  <div class="vuelo-card vuelo-ida-href" data-id="{{ vuelo.id }}" onclick="window.location=\'/vuelos/seleccionar/{{ vuelo.id }}/\'">'
new = '  <div class="vuelo-card vuelo-ida-href" data-id="{{ vuelo.id }}" onclick="seleccionarIda({{ vuelo.id }}, this)">'

content = content.replace(old, new)

old2 = "  <a href=\"{% url 'seleccionar_vuelo' vuelo.id %}\" class=\"vuelo-seleccionar\">\n        Seleccionar \u203a\n      </a>"
new2 = "  <button class=\"vuelo-seleccionar\" onclick=\"event.stopPropagation(); seleccionarIda({{ vuelo.id }}, this.closest('.vuelo-card'))\">Seleccionar \u203a</button>"

content = content.replace(old2, new2)

old_js = 'function seleccionarRegreso(vuelo_regreso_id, card) {'
new_js = '''var idaSeleccionada = null;

function seleccionarIda(vuelo_id, card) {
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
}

function seleccionarRegreso(vuelo_regreso_id, card) {'''

content = content.replace(old_js, new_js)

old_link = "  link.href = '/vuelos/seleccionar/' + idaId + '/?vuelo_regreso_id=' + vuelo_regreso_id;"
new_link = "  link.href = '/vuelos/seleccionar/' + idaSeleccionada + '/?vuelo_regreso_id=' + vuelo_regreso_id;"
content = content.replace(old_link, new_link)

# Agregar mensaje entre secciones ida y regreso
old_regreso_title = "  <h3 style=\"font-family:var(--font-serif);font-size:1.2rem;color:var(--text-muted);margin:2rem 0 1rem\">\u21a9 Vuelos de regreso</h3>"
new_regreso_title = """  <div id="msg-selecciona-regreso" style="display:none;background:#FFF3CD;border:1px solid #C8A030;border-radius:10px;padding:1rem;margin:1.5rem 0;text-align:center;color:#8B5A00">
    <strong>Paso 2:</strong> Ahora selecciona tu vuelo de regreso
  </div>
  <h3 style="font-family:var(--font-serif);font-size:1.2rem;color:var(--text-muted);margin:2rem 0 1rem">\u21a9 Vuelos de regreso</h3>"""
content = content.replace(old_regreso_title, new_regreso_title)

open('AEROLINEA/templates/luxair/buscar_vuelos.html', 'w', encoding='utf-8').write(content)
print('Listo!')
