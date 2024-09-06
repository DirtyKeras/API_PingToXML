import csv
from ping3 import ping
from xml.etree.ElementTree import ElementTree, Element, SubElement
from re import compile
from time import sleep

# Global variables
#Nombre de como guarfar el xml
nombre_archivo_xml = "./files/ping_result.xml"
# Ruta al archivo CSV con direcciones IP
csv_file_path = './files/ips.csv'


# Función para hacer ping a una IP y retornar el tiempo de respuesta
def ping_ip(ip_address):
    return ping(ip_address)

def is_valid_ipv4(ip):
    pattern = compile(r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' 
                         r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' 
                         r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' 
                         r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    return pattern.match(ip) is not None

# Devuelve una lisra con la IPs, desde un archivo CSV
def read_ips_from_csv(file_path):
    ips = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            ips.append(row[0])
    return ips

# Crear el árbol XML a partir de los resultados del ping
def create_xml_from_results(results):
    #Elemento root
    root = Element("PingResults")
    for ip, response_time in results.items():
        # Crear un elemento para cada IP
        ip_element = SubElement(root, "IP_" + str(ip).replace(".", "_"))
        SubElement(ip_element, "Address").text = ip
        SubElement(ip_element, "ResponseTime").text = str(response_time)
    
    # Crear el árbol XML y lo guardamos
    try:
        tree = ElementTree(root)
        tree.write(nombre_archivo_xml)
    except():
        print("No se pudo escribir el archivo")

#Función para ejecutar constantemente
def monitor_ips():
    ip_addresses = read_ips_from_csv(csv_file_path)
    ping_results = {}

    for ip in ip_addresses:
        if is_valid_ipv4(ip):
            response_time = ping_ip(ip)
            ping_results[ip] = response_time if response_time is not None else 'No response'

    create_xml_from_results(ping_results)

if __name__ == '__main__':
    try:
        while True:
            monitor_ips()
            sleep(5)  # Ejecutar cada minuto
    except KeyboardInterrupt:
        print("Stopping monitoring...")
