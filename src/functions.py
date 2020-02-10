#--------------------- Transformación del parámnetro localización para poder generar geoQuerys -----------------------
def asGeoJSON(lat,lng):
    try:
        lat = float(lat)
        lng = float(lng)
        if not math.isnan(lat) and not math.isnan(lng):
            return {
                "type":"Point",
                "coordinates":[lng,lat]
            }
    except Exception:
        print("Invalid data")
        return None

#------ Generación de la consulta a Geocode y query para filtrar por distancias respecto al punto anterior -------------
def geocode(address):
    data = requests.get(f"https://geocode.xyz/{address}?json=1").json()
    print(data)
    return {
        "type":"Point",
        "coordinates":[float(data["longt"]),float(data["latt"])]
    }


def withGeoQuery(location,maxDistance=10000,minDistance=0,field="location"):
    return {
       field: {
         "$near": {
           "$geometry": location if type(location)==dict else geocode(location),
           "$maxDistance": maxDistance,
           "$minDistance": minDistance
         }
       }
    }

#---------------------------- Scrapping para sacar los índices de calidad de vida por país -----------------------------

def procesaIndices(fila):
    m = fila.find_all("td")
    #print(m[2])
    return {
        "country":m[1].text.strip(),
        "calidad_vida":float((m[2].text).replace(',','.')),
        "poder_adquisitivo":float((m[3].text).replace(',','.')),
        "seguridad":float((m[4].text).replace(',','.')),
        "costo_vida":float((m[5].text).replace(',','.')),
        "relacion_precio_vs_ingresos":float((m[6].text).replace(',','.')),
        "tiempo_desplazamiento":float((m[7].text).replace(',','.')),
        "contaminación":float((m[8].text).replace(',','.')),
        "clima":float((m[9].text).replace(',','.'))
    }

#---------------------------- GooglePlace Request -----------------------------

import os
from dotenv import load_dotenv
load_dotenv('src/.env')

def requestGooglePlace(place):
    token = os.getenv("API_GOOGLE_KEY")
    #print(token)
    if not token:
        raise ValueError("Necesitas un API_GOOGLE_KEY")
    
    baseUrl = "https://maps.googleapis.com/"
    endpoint="maps/api/place/textsearch/json"
    url = baseUrl+endpoint
    print(f"Requesting data from {url}")
    params = {
        "query":f"{place}",
        "key": f"{token}"
    }
    res = requests.get(url,params=params)
    if res.status_code != 200:
        print(res.text)
        raise ValueError("Bad Response")
    return res.json()