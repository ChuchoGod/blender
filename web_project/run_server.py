import http.server
import socketserver
import webbrowser
import os

PORT = 8000
DIRECTORY = r"c:\paginas_webs\blender\web_project"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

print(f"Iniciando servidor en http://localhost:{PORT}")
print(f"Sirviendo archivos desde: {DIRECTORY}")
print("Presiona Ctrl+C para detener el servidor.")

# Abrir el navegador automáticamente
webbrowser.open(f"http://localhost:{PORT}/index.html")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
