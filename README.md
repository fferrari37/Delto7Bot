Este es un proyecto de un bot de Telegram desarrollado con Python que utiliza tres APIs externas para ofrecer funcionalidades, como consultar el clima, realizar análisis de sentimientos y gestionar un contador.

## Módulos

- **Consulta del clima:** Permite al usuario consultar el clima actual en una ciudad específica, junto a algún dato relevante sobre dicha ciudad y una recomendación de 3 restaurantes a visitar. 
- **Gestión de un contador:** Permite al usuario incrementar y consultar su contador personal.
- **Análisis de sentimientos:** Permite analizar el sentimiento de una conversación y se clasificará como positivo, negativo o neutral, proporcionando el motivo del resultado.

## Requisitos

- Python 3.8 o superior.
- Dependencias de Python (instalables con pip):
  - **pyTelegramBotAPI** (pip install pyTelegramBotAPI)
  - **openai** (pip install openai)
  - **requests** (pip install requests)
  - **python-dotenv** (pip install python-dotenv)
- Claves de API necesarias:
  - **Telegram Bot Token**: Token necesario para interactuar con Telegram.
  - **OpenWeather API Key**: API Key neceasria para obtener los datos climáticos de la request.
  - **OpenAI API Key**: API Key necesaria para poder solicitarle a ChatGPT el análisis de sentimientos de una conversación.
  - **Google Places API Key**: API Key necesaria para obtener la recomendación de 3 restaurantes en la ciudad donde se consultó el clima.


## Instalación

1. Clonar el repositorio:
   `bash`
   - git clone https://github.com/fferrari37/Delto7Bot.git
   - cd Delto7Bot

2. Crear un entorno virtual:
   `bash`
   - python -m venv venv
   

3. Activar el entorno virtual:
   ## En Windows:
     `bash`
     - .\venv\Scripts\activate

4. Instalar las dependencias necesarias que fueron mencionadas al prinicio:
   `bash`
   - pip install <dependencia>


5. Crear y configurar un archivo `.env` en la raíz del proyecto:
   ## .env
   TELEGRAM_TOKEN = <Token propio de Telegram>
   APIKEY_OPENWEATHER = <API Key propia de OpenWeather> 
   APIKEY_OPENAI = <API Key propia de OpenAI>
   GOOGLE_PLACES_APIKEY = <API Key propia de Google Places>
   

6. Inicia el bot:
   ## bash
   - python main.py

## Uso

1. **Comando `/start`:**
   - Muestra un menú de opciones para seleccionar entre:
     - ¡Quiero saber el clima! ☀
     - ¡Quiero contar! 🔢
     - Analizar conversacion 🗯

2. **"¡Quiero saber el clima! ☀":**
   - Proporciona el nombre de una ciudad y el bot devolverá información climática actual de una ciudad especificada, algun dato relevante de la misma y una recomendación de 3 restaurantes en la ciudad a los cuales el usuario pueda concurrir. 
   La recomendación de los restaurantes parte de la idea de que generalmente el clima es un condicionante para desarrollar distintas actividades y que generalmente se consulta sobre la ciudad en la que la persona se encuentra. El objetivo es brindar algunas opciones donde el usuario pueda concurrir almorzar si considera que el estado del tiempo es aprovechable.  

3. **¡Quiero contar! 🔢**
   - Gestiona un contador propio del usuario donde, al selecionarlo, incrementará su valor y se devolvera al usuario el total del mismo.

4. **Analizar conversacion 🗯**
   - Permite proporcionar una conversación con la cual sera analizada por IA y devolvera si el sentimiento de la misma es Positivo, Negativo o Neutral y a su vez se comentará el motivo de porque se llego a esa conclusión.

