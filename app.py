from flask import Flask, Response, request
import requests
import os

app = Flask(__name__)

# --- CONFIGURACIÓN ---
WEBDAV_URL = os.environ.get('WEBDAV_URL')
WEBDAV_USERNAME = os.environ.get('WEBDAV_USERNAME')
WEBDAV_PASSWORD = os.environ.get('WEBDAV_PASSWORD')

# <--- AÑADIDO PARA DEBUG: Imprimir la URL base al iniciar para verificarla
print(f"INFO: Iniciando la aplicación con WEBDAV_URL: {WEBDAV_URL}")

@app.route('/pdf', methods=['GET'])
def get_pdf():
    # Obtener el nombre del archivo desde el parámetro 'name'
    file_name = request.args.get('name')
    
    # <--- AÑADIDO PARA DEBUG: Ver qué archivo se está pidiendo
    print(f"DEBUG: Petición recibida para el archivo: '{file_name}'")

    if not file_name:
        print("ERROR: Parámetro 'name' no fue proporcionado en la petición.")
        return Response("Error: 'name' parameter is required", status=400)

    # Construir la URL completa del archivo
    # Asegurémonos de que la URL base termine con / y el nombre no empiece con /
    file_url = f"{WEBDAV_URL.rstrip('/')}/{file_name.lstrip('/')}"
    
    # <--- AÑADIDO PARA DEBUG: Ver la URL exacta que se va a solicitar
    print(f"DEBUG: Intentando acceder a la URL: {file_url}")

    try:
        # Hacer la solicitud autenticada al WebDAV
        response = requests.get(file_url, auth=(WEBDAV_USERNAME, WEBDAV_PASSWORD), stream=True)
        response.raise_for_status()  # Lanza un error si la solicitud falla (ej. 404 Not Found, 401 Unauthorized)

        # <--- AÑADIDO PARA DEBUG: Confirmar que la descarga fue exitosa
        print(f"SUCCESS: Archivo '{file_name}' descargado correctamente (status: {response.status_code}). Enviando respuesta.")

        # Devolver el contenido del PDF como respuesta
        return Response(
            response.content,
            content_type='application/pdf',
            headers={'Content-Disposition': f'inline; filename="{file_name}"'}
        )

    except requests.exceptions.HTTPError as http_err:
        # <--- AÑADIDO PARA DEBUG: Capturar errores HTTP específicos (como 404)
        print(f"HTTP ERROR: No se pudo acceder a '{file_url}'. Status: {http_err.response.status_code}. Response: {http_err.response.text}")
        return Response(f"Error: No se pudo encontrar el archivo o el acceso fue denegado. Status: {http_err.response.status_code}", status=http_err.response.status_code)
        
    except requests.exceptions.RequestException as e:
        # <--- AÑADIDO PARA DEBUG: Capturar otros errores de red o conexión
        print(f"REQUEST ERROR: Fallo al intentar conectar con WebDAV. Error: {str(e)}")
        return Response(f"Error accessing WebDAV: {str(e)}", status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)