from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("WEATHER_API_KEY")

def fetch_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    r = requests.get(url, params=params, timeout=5)
    if r.status_code != 200:
        return None
    data = r.json()
    return {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data.get("wind", {}).get("speed", 0),
        "visibility": data.get("visibility", 10000) / 1000  # Convert to km
    }

def get_weather_alerts(weather_data):
    alerts = []
    temp = weather_data["temp"]
    feels_like = weather_data["feels_like"]
    humidity = weather_data["humidity"]
    wind_speed = weather_data["wind_speed"]
    visibility = weather_data["visibility"]
    description = weather_data["description"].lower()
    
    # Temperature alerts
    if temp >= 35:
        alerts.append({
            "type": "danger",
            "icon": "🔥",
            "title": "Extreme Heat Warning",
            "message": "Temperature is dangerously high. Stay hydrated, avoid prolonged sun exposure, and seek air conditioning."
        })
    elif temp <= -10:
        alerts.append({
            "type": "danger", 
            "icon": "🥶",
            "title": "Extreme Cold Warning",
            "message": "Dangerously cold conditions. Limit outdoor exposure and dress in multiple layers."
        })
    elif temp >= 30:
        alerts.append({
            "type": "warning",
            "icon": "🌡️",
            "title": "Heat Advisory",
            "message": "Very hot weather. Stay hydrated and take breaks in shade."
        })
    elif temp <= 0:
        alerts.append({
            "type": "warning",
            "icon": "❄️",
            "title": "Freezing Conditions",
            "message": "Below freezing temperatures. Watch for icy conditions."
        })
    
    # Feels like temperature
    if abs(feels_like - temp) > 5:
        if feels_like > temp:
            alerts.append({
                "type": "info",
                "icon": "🌡️",
                "title": "Feels Hotter",
                "message": f"Feels like {feels_like:.1f}°C due to humidity. Dress lighter than temperature suggests."
            })
        else:
            alerts.append({
                "type": "info",
                "icon": "💨",
                "title": "Feels Colder", 
                "message": f"Feels like {feels_like:.1f}°C due to wind chill. Dress warmer than temperature suggests."
            })
    
    # Humidity alerts
    if humidity >= 80:
        alerts.append({
            "type": "warning",
            "icon": "💧",
            "title": "High Humidity",
            "message": "Very humid conditions. You may feel hotter than actual temperature."
        })
    elif humidity <= 20:
        alerts.append({
            "type": "info",
            "icon": "🏜️",
            "title": "Low Humidity",
            "message": "Very dry air. Stay hydrated and consider using moisturizer."
        })
    
    # Wind alerts
    if wind_speed >= 15:  # > 54 km/h
        alerts.append({
            "type": "warning",
            "icon": "💨",
            "title": "Strong Winds",
            "message": "High wind speeds. Secure loose items and be cautious outdoors."
        })
    elif wind_speed >= 10:  # > 36 km/h
        alerts.append({
            "type": "info",
            "icon": "🌬️",
            "title": "Windy Conditions",
            "message": "Moderate winds. Consider wind-resistant clothing."
        })
    
    # Visibility alerts
    if visibility < 1:
        alerts.append({
            "type": "danger",
            "icon": "🌫️",
            "title": "Very Poor Visibility",
            "message": "Extremely limited visibility. Avoid driving if possible."
        })
    elif visibility < 5:
        alerts.append({
            "type": "warning",
            "icon": "🌁",
            "title": "Poor Visibility",
            "message": "Reduced visibility due to fog or haze. Drive carefully."
        })
    
    # Weather condition alerts
    if 'thunderstorm' in description:
        alerts.append({
            "type": "danger",
            "icon": "⛈️",
            "title": "Thunderstorm Alert",
            "message": "Thunderstorms in the area. Stay indoors and avoid open areas."
        })
    elif 'heavy rain' in description or 'downpour' in description:
        alerts.append({
            "type": "warning",
            "icon": "🌧️",
            "title": "Heavy Rain Warning",
            "message": "Heavy rainfall expected. Watch for flooding and carry waterproof gear."
        })
    elif 'blizzard' in description or 'heavy snow' in description:
        alerts.append({
            "type": "danger",
            "icon": "🌨️",
            "title": "Heavy Snow Alert",
            "message": "Heavy snowfall conditions. Avoid unnecessary travel."
        })
    
    return alerts

def recommend_outfit(weather_data, alerts):
    temp = weather_data["temp"]
    description = weather_data["description"]
    humidity = weather_data["humidity"]
    wind_speed = weather_data["wind_speed"]
    
    suggestions = []
    
    # Base temperature rules
    if temp >= 30:
        suggestions += ['light shorts', 'tank top', 'sunglasses', 'sunhat']
    elif temp >= 25:
        suggestions += ['shorts', 't-shirt', 'sunglasses']
    elif temp >= 20:
        suggestions += ['light jeans', 'short-sleeve shirt']
    elif temp >= 15:
        suggestions += ['jeans', 'long-sleeve shirt']
    elif temp >= 10:
        suggestions += ['pants', 'sweater', 'light jacket']
    elif temp >= 0:
        suggestions += ['warm pants', 'hoodie', 'jacket']
    else:
        suggestions += ['thermal wear', 'heavy coat', 'winter boots', 'gloves']
    
    # Weather condition adjustments
    if 'rain' in description.lower():
        suggestions += ['umbrella', 'raincoat', 'waterproof shoes']
    elif 'snow' in description.lower():
        suggestions += ['snow boots', 'warm gloves', 'scarf', 'hat']
    elif 'thunderstorm' in description.lower():
        suggestions += ['stay indoors', 'waterproof jacket']
    
    # Wind adjustments
    if wind_speed >= 10:
        suggestions += ['windbreaker', 'secure hat']
    
    # Humidity adjustments
    if humidity >= 70 and temp >= 20:
        suggestions += ['breathable fabrics', 'moisture-wicking clothes']
    
    # Alert-based suggestions
    for alert in alerts:
        if alert["type"] == "danger" and "heat" in alert["title"].lower():
            suggestions += ['cooling towel', 'electrolyte drinks']
        elif alert["type"] == "danger" and "cold" in alert["title"].lower():
            suggestions += ['hand warmers', 'insulated boots']
    
    # Remove duplicates while preserving order
    seen = set()
    unique_suggestions = []
    for item in suggestions:
        if item not in seen:
            seen.add(item)
            unique_suggestions.append(item)
    
    return unique_suggestions

@app.route('/')
def home():
    return render_template("city_form.html")

@app.route("/search_cities")
def search_cities():
    query = request.args.get('q', '')
    if len(query) < 3:
        return jsonify([])
    
    url = "https://api.openweathermap.org/geo/1.0/direct"
    params = {"q": query, "limit": 5, "appid": API_KEY}
    resp = requests.get(url, params=params, timeout=5)
    data = resp.json()
    
    cities = []
    for c in data:
        cities.append({
            "name": c["name"],
            "country": c["country"],
            "display": f"{c['name']}, {c['country']}"
        })
    
    return jsonify(cities)

@app.route("/weather")  
def weather():
    city = request.args.get('city')
    if not city:
        return render_template("city_form.html")
    
    weather_data = fetch_weather(city)
    if not weather_data:
        return render_template("city_form.html", error=f"Could not find weather for '{city}'. Please check the spelling and try again.")
    
    alerts = get_weather_alerts(weather_data)
    suggestions = recommend_outfit(weather_data, alerts)
    
    return render_template("weather.html", data=weather_data, suggestions=suggestions, alerts=alerts)

if __name__ == '__main__':
    app.run(debug=True)