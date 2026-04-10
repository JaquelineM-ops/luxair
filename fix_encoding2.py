content = open('AEROLINEA/templates/luxair/buscar_vuelos.html', encoding='utf-8').read()
fixes = {
    'â€º':'›', 'âœˆ':'✈', 'âœ¦':'✦', 'â‡„':'⇄', 'â†©':'↩',
    'Ã³':'ó', 'Ã©':'é', 'Ã¡':'á', 'Ã­':'í', 'Ãº':'ú',
    'Ã±':'ñ', 'Â¡':'¡', 'Â¿':'¿', 'Ã ':'à', 'â€"':'—',
    'Ã‚°':'°', 'Â°':'°', 'Ã‰':'É', 'Ã"':'Ó',
}
for bad, good in fixes.items():
    content = content.replace(bad, good)
open('AEROLINEA/templates/luxair/buscar_vuelos.html', 'w', encoding='utf-8').write(content)
print('Listo!')
