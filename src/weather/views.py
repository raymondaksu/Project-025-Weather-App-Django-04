from django.shortcuts import redirect, render
from decouple import config
import requests
from pprint import pprint

from .forms import CityForm
from .models import City
from django.contrib import messages

def index(request):
    form = CityForm()
    cities = City.objects.all()
    url = config("BASE_URL")

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data["name"]
            if not City.objects.filter(name=new_city).exists():
                res = requests.get(url.format(new_city))
                if res.status_code == 200:
                    form.save()
                    messages.success(request, "City added successfully!")
                else:
                    messages.warning(request, "City does not exist.")
            else:
                messages.warning(request, "City already exist.")
            return redirect("home")

    city_data = []
    for city in cities:
        res = requests.get(url.format(city))
        content = res.json()

        weather_data = {
        "city" : city.name,
        "temp" : content["main"]["temp"],
        "description" : content["weather"][0]["description"],
        "icon" : content["weather"][0]["icon"]
    }
        city_data.append(weather_data)

    context = {
        "city_data" : city_data,
        "form" : form
    }
    return render(request, "weather/index.html", context)
