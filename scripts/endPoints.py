from flask import Flask, Response

app = Flask(__name__)

@app.route('/xml')
def get_xml():
    # Ruta al archivo XML en tu sistema
    filepath = './files/ping_result.xml'

    # Leer el contenido del archivo XML
    with open(filepath, 'r') as file:
        xml_content = file.read()

    # Devolver el contenido XML como una respuesta
    return Response(xml_content, mimetype='application/xml')

if __name__ == '__main__':
    app.run()
