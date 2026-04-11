content = open("AEROLINEA/views.py", encoding="utf-8").read()

old = "        if nombre and email and telefono and num_pas:\n            messages.success(request, '\u00a1Tu solicitud grupal fue enviada! Un agente LUX AIR te contactar\u00e1 pronto. \U0001f31f')\n            return redirect('inicio')"

new = "        if nombre and email and telefono and num_pas:\n            from .models import SolicitudGrupal\n            SolicitudGrupal.objects.create(\n                usuario=request.user if request.user.is_authenticated else None,\n                nombre_contacto=nombre,\n                email=email,\n                telefono=telefono,\n                num_pasajeros=int(num_pas),\n                comentarios=comentarios,\n            )\n            messages.success(request, '\u00a1Tu solicitud grupal fue enviada! Un agente LUX AIR te contactar\u00e1 pronto. \U0001f31f')\n            return redirect('inicio')"

result = content.replace(old, new)
if result == content:
    print("NO encontrado")
else:
    open("AEROLINEA/views.py", "w", encoding="utf-8").write(result)
    print("Listo!")
