import openai
import re
from bot import bot


#Mediante ChatGTP-4 analiza el sentimiento de una conversacion en cuanto si es positivo, negativo o neutro y brinda su argumento.
def analizar_sentimientos(conversacion):
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Analizar los sentimientos de una conversación."},
                {"role": "user", "content": f"Podrias analizar el sentimiento de la conversación y clasificarlo explicitamente como 'Positivo', 'Negativo' o 'Neutral' y proporcona una breve explicacion del porque.\n\nConversación:\n{conversacion}"}
            ],
            max_tokens=70
        )
        motivo = respuesta.choices[0].message["content"].strip()
        
        if re.search(r"\bpositivo\b", motivo, re.IGNORECASE):
            sentimiento = "Positivo"
        elif re.search(r"\bnegativo\b", motivo, re.IGNORECASE):
            sentimiento = "Negativo"
        else:
            sentimiento = "Neutral"
        return sentimiento, motivo
    except openai.error.OpenAIError as e:
        raise e
    

#Funcion para el retorno al usuario del analisis realizado.
def analizar_conversacion(mensaje):
    conversacion = mensaje.text
    
    try:
        sentimiento, motivo = analizar_sentimientos(conversacion)
        bot.send_message(mensaje.chat.id, f"El sentimiento en la conversacion es: {sentimiento}")
        bot.send_message(mensaje.chat.id, f"Motivo de esta conclusión: {motivo}")
    except openai.error.OpenAIError as e:
        bot.send_message(mensaje.chat.id, "No se pudo analizar la conversacion.")