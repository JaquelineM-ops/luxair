content = open('AEROLINEA/templates/luxair/confirmacion.html', encoding='utf-8').read()
fixes = {
    'Ã¡':'á','Ã©':'é','Ã­':'í','Ã³':'ó','Ãº':'ú',
    'Ã±':'ñ','Â¡':'¡','Â¿':'¿','Ã‰':'É','Ã"':'Ó',
    'âœ¦':'✦','âœˆ':'✈','â€"':'—','Ã ':'à',
}
for bad, good in fixes.items():
    content = content.replace(bad, good)
open('AEROLINEA/templates/luxair/confirmacion.html', 'w', encoding='utf-8').write(content)
print('Listo!')
