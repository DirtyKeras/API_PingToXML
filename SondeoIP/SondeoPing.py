from csv import reader
from ping3 import ping
from xml.etree.ElementTree import ElementTree, Element, SubElement
from re import compile

# Variables globales (ajusta las rutas si es necesario)
xml_file_path = "./files/ping_result.xml"
csv_file_path = './files/ips.csv'
tiempo_espera_ping = 2.0

# Función de ping
# Función para hacer ping a una IP y retornar "true" o "false"

def ping_ip(ip_address):
    response_time = ping(ip_address, timeout=tiempo_espera_ping)
    if (response_time is None) or (response_time == False and (str(response_time) != "0.0")):  # Si el ping es fallido
        print(f"{ip_address}  :  FALLAAAAAAAA - {response_time}") #Linea de log por consola
        return "false"
    else:  # Si el ping es exitoso
        print(f"{ip_address}  :  {response_time}") #Linea de log por consola
        return "true"

def is_valid_ipv4(ip):
    pattern = compile(r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' 
                        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' 
                        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' 
                        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    return pattern.match(ip) is not None

def read_ips_from_csv(file_path):
    ips = []
    with open(file_path, mode='r') as file:
        csvFile = reader(file)
        for row in csvFile:
            ips.append(row[0])
    return ips

def create_xml_from_results(results):
    root = Element("PingResults")
    print("-----------------------------------------------")
    for ip, response_time in results.items():
        ip_element = SubElement(root, "IP_" + str(ip).replace(".", "_"))
        SubElement(ip_element, "Address").text = ip
        SubElement(ip_element, "ResponseTime").text = str(response_time)
    
    try:
        tree = ElementTree(root)
        tree.write(xml_file_path)
    except:
        print("No se pudo escribir el archivo")

# Función que sensa todas las ips y guarda el estado en un archivo xml:
def sondear_ips():
    ip_addresses = read_ips_from_csv(csv_file_path)
    ping_results = {}

    for ip in ip_addresses:
        if is_valid_ipv4(ip):
            ping_results[ip] = ping_ip(ip)

    create_xml_from_results(ping_results)
