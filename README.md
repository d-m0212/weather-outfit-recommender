# Weather Outfit Recommender

A web application that provides intelligent outfit recommendations based on real-time weather data for any city worldwide. Built as a practical tool to solve the daily problem of deciding what to wear.

## What it does

- Get weather-based outfit suggestions for any city globally
- Real-time weather data with comprehensive conditions analysis
- Smart city search with autocomplete functionality
- Dynamic backgrounds that change based on weather conditions
- Mobile-responsive design that works on all devices

## Why I built this

I wanted to create a practical daily-use application that combines weather data with intelligent decision-making. This tool helps people make better clothing choices whether they're at home or traveling to new cities.

## Technologies Used

- **Python** with Flask for the web server
- **OpenWeatherMap API** for real-time weather data and city geocoding
- **JavaScript** for dynamic autocomplete and user interactions
- **HTML/CSS** with responsive design and weather-adaptive styling
- **Algorithm development** for outfit recommendation logic

## How to run it

1. **Download the project**

```
git clone <repository-url>
cd weather-outfit-recommender
```

2. **Set up Python environment**

```
python -m venv venv
venv\Scripts\activate
```

3. **Install required packages**

```
pip install -r requirements.txt
```

4. **Get API key**
- Sign up at [OpenWeatherMap](https://openweathermap.org/api)
- Get your free API key from the dashboard
- Create a `.env` file and add your credentials:

```
WEATHER_API_KEY=your_api_key_here
```

5. **Start the application**

```
python app.py
```

6. **Open your browser** and go to `http://127.0.0.1:5000`

## How to use

1. Type any city name in the search box (autocomplete will help you)
2. Select your city from the suggestions
3. Click "Get Weather & Outfit" 
4. View the current weather conditions and personalized outfit recommendations
5. The background and colors adapt to match the weather conditions

## What I learned

- Building recommendation algorithms with multiple decision factors
- Working with REST APIs and handling real-time data
- Creating responsive web interfaces with dynamic styling
- Implementing autocomplete functionality with debounced search
- Managing environment variables and API keys securely
- Global application design that works for international users

## Challenges faced

- Creating intelligent outfit logic that considers multiple weather factors
- Implementing smooth city autocomplete without overwhelming the API
- Designing weather-responsive UI that provides visual context
- Handling edge cases and API failures gracefully
- Making the algorithm work across different global climates

## Future improvements

- User preference settings for style and color choices
- Weather alerts and severe condition warnings  
- Saved favorite cities for quick access
- Social sharing of outfit recommendations
- Mobile app version

---

**Note**: This project demonstrates full-stack development skills and practical problem-solving. The recommendation algorithm considers temperature, humidity, precipitation, and wind conditions to provide useful daily guidance.



