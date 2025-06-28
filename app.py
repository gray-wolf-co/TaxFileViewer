from flask import Flask, Response, request
import requests
import os

app = Flask(__name__)

# Obtener configuración desde variables de entorno
WEBDAV_URL = os.environ.get('WEBDAV_URL')  # Ejemplo: https://tudominio.com/webdav/
WEBDAV_USERNAME = os.environ.get('WEBDAV_USERNAME')
WEBDAV_PASSWORD = os.environ.get('WEBDAV_PASSWORD')

@app.route('/pdf', methods=['GET'])
def get_pdf():
    # Obtener el nombre del archivo desde el parámetro 'name'
    file_name = request.args.get('name')
    if not file_name:
        return Response("Error: 'name' parameter is required", status=400)

    # Construir la URL completa del archivo
    file_url = f"{WEBDAV_URL}{file_name}"

    try:
        # Hacer la solicitud autenticada al WebDAV
        response = requests.get(file_url, auth=(WEBDAV_USERNAME, WEBDAV_PASSWORD), stream=True)
        response.raise_for_status()  # Lanza un error si la solicitud falla

        # Devolver el contenido del PDF como respuesta
        return Response(
            response.content,
            content_type='application/pdf',
            headers={'Content-Disposition': f'inline; filename="{file_name}"'}
        )

    except requests.exceptions.RequestException as e:
        return Response(f"Error accessing WebDAV: {str(e)}", status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)