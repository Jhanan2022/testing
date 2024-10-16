import requests, ipaddress

def es_ip_valida(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def get_location(ip):
    if not es_ip_valida(ip):
        raise ValueError("IP no válida")
    
    url =  f"http://freeipapi.com/api/json/{ip}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    #import ipdb; ipdb.set_trace()
    return {
        "countryName": data["countryName"],
        "cityName": data["cityName"],
        "regionName": data["regionName"],
        "countryCode": data["countryCode"],
    }
