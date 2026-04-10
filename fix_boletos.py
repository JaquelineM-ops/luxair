content = open('AEROLINEA/templates/luxair/mis_boletos.html', encoding='utf-8').read()
old = '''<div style="width:80px;height:80px;background:var(--midnight);border-radius:6px;display:flex;align-items:center;justify-content:center;color:var(--champagne);font-size:.55rem;text-align:center;padding:.5rem;word-break:break-all">
            {{ boleto.codigo_boleto|stringformat:"s"|slice:":16" }}
          </div>'''
new = '<img src="https://api.qrserver.com/v1/create-qr-code/?size=80x80&data={{ boleto.codigo_boleto }}" width="80" height="80" style="border-radius:6px">'
content = content.replace(old, new)
open('AEROLINEA/templates/luxair/mis_boletos.html', 'w', encoding='utf-8').write(content)
print('Listo!')
