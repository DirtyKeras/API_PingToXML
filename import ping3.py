import ping3
import xml.etree.ElementTree as ET

# Dirección IP a la que se hará ping
ip_address = "192.168.1.24"

# Realizar el ping
response_time = ping3.ping(ip_address)

# Crear el elemento raíz del XML
root = ET.Element("PingResult")

# Añadir subelementos con los resultados
ET.SubElement(root, "IPAddress").text = ip_address
ET.SubElement(root, "ResponseTime").text = str(response_time)

# Crear el árbol XML y guardarlo en un archivo
tree = ET.ElementTree(root)
tree.write("ping_result.xml")

print(f"Ping a {ip_address} completado. Response Timm {str(response_time)}")