


# Django Weather Project Setup Guide

## 1. Set Up Your Local Development Environment

### Install Python

Ensure Python 3.x is installed on your computer. You can download it from [python.org](https://www.python.org/).

### Create a Virtual Environment

Open your terminal (Command Prompt, PowerShell, or terminal on Mac/Linux) and navigate to the directory where you want to create your project.

Run the following commands:

```bash
python -m venv myenv
```

On Windows, activate the virtual environment using:

```bash
myenv\Scripts\activate
```

### Install Django and Other Dependencies

With the virtual environment activated, install Django and other required packages:

```bash
pip install django
pip install requests
pip install pytz  # For converting Unix timestamps to readable format.
```

---

## 2. Create a New Django Project

### Start a New Project

Create a new Django project by running:

```bash
django-admin startproject weather_project
cd weather_project
```

### Create a New Django App

Inside your project directory, create a new app called `weather`:

```bash
python manage.py startapp weather
```

### Add the App to Your Project

Open `weather_project/settings.py` and add `'weather'` to the `INSTALLED_APPS` list:

```python
INSTALLED_APPS = [
    ...
    'weather',
]
```

---

## 3. Create the Weather-Checking Functionality

### Get a Weather API Key

Sign up for a free API key from a weather service provider such as [OpenWeatherMap](https://openweathermap.org/api) or [WeatherAPI](https://www.weatherapi.com/).

### Create a View to Fetch Weather Data

Open `weather/views.py` and create a view to fetch weather data:

```python
import requests
from django.shortcuts import render

def get_weather(request):
    city = request.GET.get('city', 'London')  # Default to London if no city is provided
    api_key = 'YOUR_API_KEY'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()

    context = {
        'city': city,
        'weather_data': weather_data,
    }
    return render(request, 'weather/weather.html', context)
```

### Set Up URL Routing

Create a `urls.py` file in the `weather` app directory and add the following:

```python
from django.urls import path
from .views import get_weather

urlpatterns = [
    path('', get_weather, name='get_weather'),
]
```

Include the `weather` app’s URLs in the project’s main `urls.py` file (`weather_project/urls.py`):

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('weather.urls')),
]
```

---

## 4. Create a Template to Display Weather Data

### Create a Template Directory

Inside the `weather` app, create a `templates/weather` directory.

### Create a Template File

Create a file named `weather.html` inside `templates/weather` with the following content:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Weather Checker</title>
</head>
<body>
    <h1>Weather in {{ city }}</h1>
    {% if weather_data %}
        <p>Temperature: {{ weather_data.main.temp }}°C</p>
        <p>Weather: {{ weather_data.weather.0.description }}</p>
    {% else %}
        <p>Could not retrieve weather data.</p>
    {% endif %}

    <form method="GET">
        <input type="text" name="city" placeholder="Enter city">
        <button type="submit">Check Weather</button>
    </form>
</body>
</html>
```

---

## 5. Run the Django Project

### Apply Migrations

Run the following command to apply migrations:

```bash
python manage.py migrate
```

### Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

### Access the Website

Open your web browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/). You should see a form where you can enter a city name to check its weather.
```

