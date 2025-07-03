from flask import Flask, Response, request
import requests
import os

app = Flask(__name__)

# Get configuration from environment variables
WEBDAV_URL = os.environ.get('WEBDAV_URL')  # Example: https://yourdomain.com/webdav/
WEBDAV_USERNAME = os.environ.get('WEBDAV_USERNAME')
WEBDAV_PASSWORD = os.environ.get('WEBDAV_PASSWORD')

@app.route('/pdf', methods=['GET'])
def get_pdf():
    # Get the file name from the 'name' query parameter
    file_name = request.args.get('name')
    if not file_name:
        return Response("Error: 'name' parameter is required", status=400)

    # Build the full file URL
    file_url = f"{WEBDAV_URL}{file_name}"

    try:
        # Make authenticated request to WebDAV server
        response = requests.get(file_url, auth=(WEBDAV_USERNAME, WEBDAV_PASSWORD), stream=True)
        response.raise_for_status()  # Raise error if request failed

        # Return the PDF content as response
        return Response(
            response.content,
            content_type='application/pdf',
            headers={'Content-Disposition': f'inline; filename="{file_name}"'}
        )

    except requests.exceptions.RequestException as e:
        return Response(f"Error accessing WebDAV: {str(e)}", status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
