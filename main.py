from flask import Flask, Response
from threading import Thread
from SondeoIP.SondeoPing import sondear_ips
from time import sleep

"""
from csv import reader
from ping3 import ping
from xml.etree.ElementTree import ElementTree, Element, SubElement
from re import compile
"""
xml_file_path = "./files/ping_result.xml"

intervalo_sondeo = 5.0 #Se realiza el sondeo con 5 segundos de espera

# Inicializar la aplicación Flask
app = Flask(__name__)

def monitoreo_ips():
    while True:
        sondear_ips()
        sleep(intervalo_sondeo)
        


# Endpoint que devuelve el XML
@app.route('/xml')
def get_xml():
    filepath = xml_file_path
    try:
        with open(filepath, 'r') as file:
            xml_content = file.read()
        return Response(xml_content, mimetype='application/xml')
    except FileNotFoundError:
        return Response("<error>XML file not found</error>", mimetype='application/xml')


# Ejecutar Flask y el monitoreo en paralelo
if __name__ == '__main__':
    # Iniciar el monitoreo en un hilo separado
    hilo_monitoreo_ips = Thread(target=monitoreo_ips)
    hilo_monitoreo_ips.daemon = True  # True - permite que el hilo se cierre cuando Flask se cierre
    hilo_monitoreo_ips.start()

    # Iniciar el servidor Flask
    app.run()
