content = open("AEROLINEA/views.py", encoding="utf-8").read()
idx = content.find("def vuelo_grupal")
print(repr(content[idx:idx+600]))
