import openai
from bot import bot
from config import apikey_openai
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from modulos.clima import clima_ciudad
from modulos.contador import incrementar_contador, obtener_contador, iniciar_db
from modulos.analisis_conv import analizar_conversacion

openai.api_key = apikey_openai

@bot.message_handler(commands=["start"])
def mensaje_de_bienvenida(mensaje):
    opciones = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    opciones.add(
        KeyboardButton("¡Quiero saber el clima! \U00002600"), 
        KeyboardButton("¡Quiero contar! \U0001F522"),
        KeyboardButton("Analizar conversacion \U0001F5EF")
    )
    bot.send_message(mensaje.chat.id, "¡Hola! ¿Que necesitas?\U0001F600", reply_markup=opciones)
    bot.register_next_step_handler(mensaje, opcion_seleccionada)


#Segun la respuesta obtenida luego de haber iniciado el bot, evalua que opcion fue la seleccionada por el usuario.
def opcion_seleccionada(mensaje):
    if mensaje.text.lower() == "¡quiero saber el clima! ☀":
        bot.send_message(mensaje.chat.id, "Sobre que ciudad le interesaria conocer el clima actual?")
        bot.register_next_step_handler(mensaje, clima_ciudad)
    elif mensaje.text.lower() == "¡quiero contar! 🔢":
        user_id = mensaje.from_user.id
        iniciar_db()
        incrementar_contador(user_id)
        contador = obtener_contador(user_id)
        bot.send_message(mensaje.chat.id, f"Contador incrementado a: {contador}")
    elif mensaje.text.lower() == "analizar conversacion 🗯":
        bot.send_message(mensaje.chat.id, "Ingrese la conversacion que desea analizar.")
        bot.register_next_step_handler(mensaje, analizar_conversacion)


bot.polling()


