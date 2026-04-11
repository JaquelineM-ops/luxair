content = open("AEROLINEA/views.py", encoding="utf-8").read()

old = """        if nombre and email and telefono and num_pas:
            messages.success(request, 'Â¡Tu solicitud grupal fue enviada! Un agente LUX AIR te contactarÃ¡ pronto. ðŸŒŸ')
            return redirect('inicio')"""

new = """        if nombre and email and telefono and num_pas:
            SolicitudGrupal.objects.create(
                usuario=request.user if request.user.is_authenticated else None,
                nombre_contacto=nombre,
                email=email,
                telefono=telefono,
                num_pasajeros=int(num_pas),
                comentarios=comentarios,
            )
            messages.success(request, '¡Tu solicitud grupal fue enviada! Un agente LUX AIR te contactará pronto.')
            return redirect('inicio')"""

result = content.replace(old, new)
if result == content:
    print("NO encontrado")
else:
    open("AEROLINEA/views.py", "w", encoding="utf-8").write(result)
    print("Listo!")
