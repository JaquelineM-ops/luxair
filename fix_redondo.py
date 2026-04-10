content = open('AEROLINEA/templates/luxair/buscar_vuelos.html', encoding='utf-8').read()

old = '''  {% for vuelo in vuelos_regreso %}
  <div class="vuelo-card">
    <div class="vuelo-main">
      <div class="vuelo-airport">
        <div class="vuelo-time">{{ vuelo.fecha_salida|time:"H:i" }}</div>
        <div class="vuelo-iata">{{ vuelo.origen.codigo_iata }}</div>
        <div class="vuelo-ciudad">{{ vuelo.origen.ciudad }}</div>
      </div>
      <div class="vuelo-middle">
        <div class="vuelo-duracion">Vuelo directo</div>
        <div class="vuelo-line">✈</div>
      </div>
      <div class="vuelo-airport">
        <div class="vuelo-time">{{ vuelo.fecha_llegada|time:"H:i" }}</div>
        <div class="vuelo-iata">{{ vuelo.destino.codigo_iata }}</div>
        <div class="vuelo-ciudad">{{ vuelo.destino.ciudad }}</div>
      </div>
      <div class="vuelo-precios">
        <div class="precio-opcion">
          <div class="precio-clase">Económica</div>
          <div class="precio-monto">${{ vuelo.precio_economica|floatformat:0 }}</div>
        </div>
        <div class="precio-opcion">
          <div class="precio-clase">Ejecutiva</div>
          <div class="precio-monto">${{ vuelo.precio_ejecutiva|floatformat:0 }}</div>
        </div>
      </div>
      <button class="vuelo-seleccionar">Seleccionar ›</button>
    </div>
    <div class="vuelo-numero">Vuelo LX{{ vuelo.numero_vuelo }} · {{ vuelo.fecha_salida|date:"d M Y" }}</div>
  </div>
  {% endfor %}'''

new = '''  {% for vuelo in vuelos_regreso %}
  <div class="vuelo-card" onclick="seleccionarRegreso({{ vuelo.id }}, this)">
    <div class="vuelo-main">
      <div class="vuelo-airport">
        <div class="vuelo-time">{{ vuelo.fecha_salida|time:"H:i" }}</div>
        <div class="vuelo-iata">{{ vuelo.origen.codigo_iata }}</div>
        <div class="vuelo-ciudad">{{ vuelo.origen.ciudad }}</div>
      </div>
      <div class="vuelo-middle">
        <div class="vuelo-duracion">Vuelo directo</div>
        <div class="vuelo-line">✈</div>
      </div>
      <div class="vuelo-airport">
        <div class="vuelo-time">{{ vuelo.fecha_llegada|time:"H:i" }}</div>
        <div class="vuelo-iata">{{ vuelo.destino.codigo_iata }}</div>
        <div class="vuelo-ciudad">{{ vuelo.destino.ciudad }}</div>
      </div>
      <div class="vuelo-precios">
        <div class="precio-opcion">
          <div class="precio-clase">Económica</div>
          <div class="precio-monto">${{ vuelo.precio_economica|floatformat:0 }}</div>
        </div>
        <div class="precio-opcion">
          <div class="precio-clase">Ejecutiva</div>
          <div class="precio-monto">${{ vuelo.precio_ejecutiva|floatformat:0 }}</div>
        </div>
        <div class="precio-opcion">
          <div class="precio-clase">1ª Clase</div>
          <div class="precio-monto">${{ vuelo.precio_primera_clase|floatformat:0 }}</div>
        </div>
      </div>
      <button class="vuelo-seleccionar" onclick="event.stopPropagation(); seleccionarRegreso({{ vuelo.id }}, this.closest('.vuelo-card'))">Seleccionar ›</button>
    </div>
    <div class="vuelo-numero">Vuelo LX{{ vuelo.numero_vuelo }} · {{ vuelo.fecha_salida|date:"d M Y" }}</div>
  </div>
  {% endfor %}
  <div id="btn-continuar-redondo" style="display:none;margin-top:1.5rem;text-align:center">
    <a id="link-continuar-redondo" href="#" class="btn btn-gold" style="padding:.9rem 2rem;font-size:1rem">
      Continuar con vuelo seleccionado ›
    </a>
  </div>'''

content = content.replace(old, new)

old_js = '''function setTrip(tipo, btn) {'''
new_js = '''function seleccionarRegreso(vuelo_regreso_id, card) {
  document.querySelectorAll('.vuelo-card').forEach(c => c.style.borderColor = '');
  card.style.borderColor = 'var(--rose)';
  // Tomar el primer vuelo de ida seleccionado
  var vueloIdaId = document.querySelector('.vuelo-ida-id') ? document.querySelector('.vuelo-ida-id').value : null;
  var cards = document.querySelectorAll('[data-vuelo-ida]');
  if(cards.length > 0) vueloIdaId = cards[0].dataset.vueloIda;
  var btnDiv = document.getElementById('btn-continuar-redondo');
  var link = document.getElementById('link-continuar-redondo');
  btnDiv.style.display = 'block';
  // El link lleva al primer vuelo de ida con el regreso como parámetro
  var primeraIda = document.querySelector('.vuelo-ida-href');
  var idaId = primeraIda ? primeraIda.dataset.id : '';
  link.href = '/vuelos/seleccionar/' + idaId + '/?vuelo_regreso_id=' + vuelo_regreso_id;
}
function setTrip(tipo, btn) {'''

content = content.replace(old_js, new_js)
open('AEROLINEA/templates/luxair/buscar_vuelos.html', 'w', encoding='utf-8').write(content)
print('Listo!')
