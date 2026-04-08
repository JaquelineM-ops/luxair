content = open('AEROLINEA/templates/luxair/confirmacion.html', encoding='utf-8').read()
fixes = {
    'ðŸ–¨':'🖨',
    'â€º':'›',
    'Â€º':'›',
    'Ã‚€º':'›',
    'MIS BOLETOS Â€°':'MIS BOLETOS ›',
    'Â°':'°',
}
for bad, good in fixes.items():
    content = content.replace(bad, good)
open('AEROLINEA/templates/luxair/confirmacion.html', 'w', encoding='utf-8').write(content)
print('Listo!')
