content = open("AEROLINEA/views.py", encoding="utf-8").read()

old = "        if nombre and email and telefono and num_pas:\n            messages.success(request, '\u00a1Tu solicitud grupal fue enviada! Un agente LUX AIR te contactar\u00e1 "

idx = content.find("if nombre and email and telefono and num_pas:")
print(f"Encontrado en: {idx}")
print(repr(content[idx:idx+200]))
