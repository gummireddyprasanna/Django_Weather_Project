import requests
from django.shortcuts import render
from datetime import datetime
import pytz
from decouple import config

def get_weather(request):
    city = request.GET.get('city', 'London')  # Default to London if no city is provided
    api_key = config('API_KEY')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()

    # Convert timestamps to readable format
    sunrise = datetime.fromtimestamp(weather_data.get('sys', {}).get('sunrise', 0), pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')
    sunset = datetime.fromtimestamp(weather_data.get('sys', {}).get('sunset', 0), pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')

    # Determine the background class based on weather condition
    weather_condition = weather_data.get('weather', [{}])[0].get('main', 'Clear')
    time_of_day = 'day' if datetime.now().hour >= 6 and datetime.now().hour < 18 else 'night'
    
    background_class = {
        'Clear': 'sunny',
        'Clouds': 'cloudy',
        'Rain': 'rainy',
        'Snow': 'snowy',
        'Thunderstorm': 'storm',
    }.get(weather_condition, 'default')  # Use 'default' if weather condition is unknown

    if time_of_day == 'night':
        background_class = f'{background_class}_night'

    detailed_data = {
        'city': city,
        'temperature': weather_data.get('main', {}).get('temp', 'N/A'),
        'weather': weather_data.get('weather', [{}])[0].get('description', 'N/A'),
        'humidity': weather_data.get('main', {}).get('humidity', 'N/A'),
        'wind_speed': weather_data.get('wind', {}).get('speed', 'N/A'),
        'pressure': weather_data.get('main', {}).get('pressure', 'N/A'),
        'sunrise': sunrise,
        'sunset': sunset,
        'background_class': background_class,
    }

    context = {
        'detailed_data': detailed_data,
    }
    return render(request, 'weather/weather.html', context)
