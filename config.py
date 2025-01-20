from dotenv import load_dotenv
import os

load_dotenv()

telegram_token = os.getenv("TELEGRAM_TOKEN")
apikey_openweather = os.getenv("APIKEY_OPENWEATHER")
apikey_openai = os.getenv("APIKEY_OPENAI")
apikey_googleplace = os.getenv("GOOGLE_PLACES_APIKEY")