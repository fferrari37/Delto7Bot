import requests
import openai
from config import apikey_openweather, apikey_googleplace
from bot import bot

#Diccionario con los ID de las distintas descripciones de cada clima para atribuir una recomendacion.
recomendaciones = {
    range(200, 233): "Evite salir si no es necesario, se esta dando una tormenta eléctrica.",
    range(300, 322): "Utilice pilot para enfrentar la llovizna.",
    range(500, 532): "No se olvide de salir con paraguas, esta lloviendo.",
    range(600, 623): "Es un buen dia para hacer angeles de nieve.",
    range(701, 782): "Intente resguardarse, la situacion climatica no es la optima.",
    781: "Concurra a un refugio, se esta dando un tornado.",
    800: "¡Es un excelente dia para pasear, no volide su protector solar!",
    range(801, 805): "No olvide llevar su paraguas por si existiera algun chubasco."
    }


#Funcion en la que se obtiene las coordenadas de la ciudad ingresada para luego hacer la consulta del clima.
def obtener_coordenadas(ciudad, state_code=None, country_code=None, limit=1):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={ciudad}"
    
    if state_code:
        url += f",{state_code}"
    if country_code:
        url += f",{country_code}"

    url += f"&limit={limit}&appid={apikey_openweather}"
    respuesta = requests.get(url)
    
    if respuesta.status_code == 200:
        data = respuesta.json()
        if data:
            latitud = data[0]["lat"]
            longitud = data[0]["lon"]
            return latitud, longitud
        else:
            return None, None
    else:
        return None, None


#Funcion que realiza la consulta del clima por la ciudad ingresada.
def obtener_clima(latitud, longitud):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitud}&lon={longitud}&appid={apikey_openweather}&units=metric&lang=es"
    respuesta = requests.get(url)
    
    if respuesta.status_code == 200:
        data = respuesta.json()
        temperatura = data["main"]["temp"]
        humedad = data["main"]["humidity"]
        descripcion_clima = data["weather"][0]["description"]
        id_clima = data["weather"][0]["id"]
        recomendacion = "No se pudo obtener una recomendacion para el clima actual."

        for id, consejo in recomendaciones.items():
            if isinstance(id, range):
                if id_clima in id:
                    recomendacion = consejo
            elif id_clima == id:
                recomendacion = consejo
        return f"""El clima actual es de {temperatura}°C, con una humedad del {humedad}%.\nDescripción del clima: {descripcion_clima}.\n{recomendacion}"""
    else:
        return f"No se ha podido obtener el clima actual, intente nuevamente."


#Funcion que obtiene 3 restaurantes recomendados para sugerir al usuario.
def top_restaurantes(ciudad):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"restaurantes en {ciudad}",
        "type": "restaurant",
        "key": apikey_googleplace
    }
    respuesta = requests.get(url, params=params)

    if respuesta.status_code == 200:
        data = respuesta.json()
        restaurantes = data.get("results", [])[:3]
        return [f"{restaurante['name']} - {restaurante.get('rating', 'N/A')} estrellas" for restaurante in restaurantes]
    else:
        return "Se produjo un error al intentar obtener los restaurantes."
    

#Funcion que traslada al usuario algun dato relevante de la ciudad al usuario, junto a la recomendacion de los restaurantes.
def respuesta_ia(mensaje, ciudad):
    try:
        request = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Generar una respuesta con algun dato relevante de una ciudad."},
                {"role": "user", "content": f"Podrias darme algo de información de {ciudad}?"}
            ],
            max_tokens=70
        )
        respuesta = request.choices[0].message["content"].strip()
        restaurantes = top_restaurantes(ciudad)
        muestra_restaurantes = "\n".join(restaurantes)
        
        if not muestra_restaurantes:
            muestra_restaurantes = "No se encontraron restaurantes."
        bot.send_message(mensaje.chat.id,f"Información adicional sobre {ciudad}:\n{respuesta} \n\nLe recomendamos 3 restaurantes a visitar:\n{muestra_restaurantes}")
    except openai.error.OpenAIError as e:
        bot.send_message(mensaje.chat.id, "No se pudo generar una respuesta.")


#Funcion que obtiene el clima de la ciudad ingresada, el cual es trasladado al usuario.
def clima_ciudad(mensaje):
    ciudad = mensaje.text
    latitud, longitud = obtener_coordenadas(ciudad)

    if latitud is not None and longitud is not None:
        clima = obtener_clima(latitud, longitud)
        bot.send_message(mensaje.chat.id, clima)
        try:
            respuesta_ia(mensaje, ciudad)
        except openai.error.OpenAIError as e:
            bot.send_message(mensaje.chat.id, f"No se pudo obtener información relevante sobre {ciudad}.")
    else:
        bot.send_message(mensaje.chat.id, f"No se encontraron las coordenadas de {ciudad}")