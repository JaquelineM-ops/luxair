content = open('AEROLINEA/templates/luxair/checkin.html', encoding='utf-8').read()
old = '    <p style="font-family:var(--font-serif);font-size:2rem;color:#8B5A00;margin-top:.75rem;letter-spacing:.15em">{{ reservacion.codigo }}</p>'
new = '''    <p style="font-family:var(--font-serif);font-size:2rem;color:#8B5A00;margin-top:.75rem;letter-spacing:.15em">{{ reservacion.codigo }}</p>
    <img src="https://api.qrserver.com/v1/create-qr-code/?size=120x120&data={{ reservacion.codigo }}" width="120" height="120" style="border-radius:8px;margin-top:1rem">'''
content = content.replace(old, new)
open('AEROLINEA/templates/luxair/checkin.html', 'w', encoding='utf-8').write(content)
print('Listo!')
