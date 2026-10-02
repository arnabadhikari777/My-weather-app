import os
import requests

from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")


@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        if not city:
            error = "Please enter a city name."

        elif not API_KEY:
            error = "API key is missing. Please check your .env file."

        else:
            url = "https://api.openweathermap.org/data/2.5/weather"

            params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }

            try:
                response = requests.get(
                    url,
                    params=params,
                    timeout=10
                )

                if response.status_code == 200:
                    data = response.json()

                    weather = {
                        "city": data["name"],
                        "country": data["sys"]["country"],
                        "temperature": round(data["main"]["temp"]),
                        "description": data["weather"][0]["description"],
                        "humidity": data["main"]["humidity"],
                        "wind_speed": data["wind"]["speed"],
                        "icon": data["weather"][0]["icon"]
                    }

                elif response.status_code == 404:
                    error = "City not found. Please check the city name."

                elif response.status_code == 401:
                    error = "Invalid API key. Please check your API key."

                else:
                    error = "Unable to get weather data. Please try again."

            except requests.exceptions.RequestException:
                error = "Network error. Please check your internet connection."

    return render_template(
        "home.html",
        weather=weather,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)