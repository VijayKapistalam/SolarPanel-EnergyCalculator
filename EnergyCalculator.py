#solar panel capacity (in watts), geographic location, panel efficiency, and installation angle.
import numpy as np
import requests as req
from datetime import date
import math
import matplotlib.pyplot as plt
import urllib.parse

#HEIGHT and WIDTH
length = input("Enter the length of the solar panel in feet (or press Enter for default): ")
while not length.isnumeric() and length != '':
    print("Invalid input! Please enter a numeric value for the panel length (or press Enter for default): ")
    length = input("Enter the length of the solar panel in feet (or press Enter for default): ")

if length == '':
    length = 5.9  # Default length in feet
else:
    length = float(length)

width = input("Enter the width of the solar panel in feet (or press Enter for default): ")
while not width.isnumeric() and width != '':
    print("Invalid input! Please enter a numeric value for the panel width (or press Enter for default):")

if width == '':
    width = 2.95  # Default width in feet
else:
    width = float(width)

panel_area = length * width


#SOLAR CAPACITY
solarCapacity = input("Enter your solar panel capacity (in watts) or press Enter for default: ")
if solarCapacity == '':
    solarCapacity = 10000  # Default solar panel capacity: 10000 watts
else:
    while not solarCapacity.isnumeric() or int(solarCapacity) < 1 or int(solarCapacity) > 50000:
        print("Invalid input! Please enter a numeric value for the solar panel capacity between 1 and 50000 watts.")
        solarCapacity = input("Enter your solar panel capacity (in watts): ")
    solarCapacity = int(solarCapacity)


#LOCATION API (Open Weather Map)
#format = http://api.openweathermap.org/geo/1.0/direct?q={city name},{state code},{country code}&limit={limit}&appid={API key}
#http://api.openweathermap.org/geo/1.0/direct?q=London&limit=5&appid={API key}
api_key = "9b1c837a6aa73b22000497c076081b37"
location = input("Enter your location (city): ")
while not location.replace(" ", "").isalpha():
    print("Invalid input! Please type in the name of the city you live in")
    location = input("Enter your location (city): ")

location_encoded = urllib.parse.quote(location)  # Encode the city name
geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location_encoded}&appid={api_key}"
response = req.get(geocoding_url)
geocoding_data = response.json()
if response.status_code == 200:
    latitude = geocoding_data[0]["lat"]
    longitude = geocoding_data[0]["lon"]
else:
    print("Failed to retrieve latitude and longitude.")


#PANEL EFFICIENCY
panelEfficiency = input("Enter your solar panel efficiency (in decimal or percentage), or press enter for the default efficiency: ")
while True:
    if panelEfficiency == '':
        panelEfficiency = 0.15  # Default efficiency (15%)
        break
    elif '%' in panelEfficiency:
        panelEfficiency = float(panelEfficiency.strip('%')) / 100
        break
    else:
        try:
            panelEfficiency = float(panelEfficiency)
            break
        except ValueError:
            print("Invalid input! Please enter a valid numeric value or percentage for the panel efficiency.")
            panelEfficiency = input("Enter your solar panel efficiency (in decimal or percentage), or press enter for the default efficiency: ")

panelEfficiency = max(0, min(panelEfficiency, 1))

#ANGLE
angle = input("Enter your installation angle in degrees (or press Enter for default): ")
if angle == '':
    angle = latitude  # Default angle: latitude tilt
else:
    while not angle.isnumeric() or float(angle) < 0 or float(angle) > 90:
        print("Invalid input! Please enter a numeric value for the installation angle between 0 and 90 degrees.")
        angle = input("Enter your installation angle in degrees: ")
    angle = float(angle)


#SOLAR IRRADIANCE API (NREL)
#/api/solar/solar_resource/v1.json?api_key=DEMO_KEY&lat=40&lon=-105
today = date.today()
current_month = today.strftime("%b").lower()

solar_API = "36wsMkVVbOApmyNzc7nCLD5vrjsqH4cb86AkKIS5"
solar_url = f"https://developer.nrel.gov/api/solar/solar_resource/v1.json?api_key={solar_API}&lat={latitude}&lon={longitude}"
solar_response = req.get(solar_url)

if solar_response.status_code == 200:
    solar_data = solar_response.json()
else:
    print("Failed to retrieve solar irradiance data.")

irradiance = solar_data["outputs"]["avg_dni"]["monthly"][f"{current_month}"]
print(end='\n')


#CALCULATIONS
print(end='\n')
incident_energy = irradiance * panel_area * math.cos(math.radians(angle))
effective_power_output = panelEfficiency * solarCapacity
energy_generation = incident_energy * effective_power_output

daily_energy_generation_kWh = energy_generation / 1000
monthly_energy_generation_kWh = (energy_generation / 1000) * 30
yearly_energy_generation_kWh = (energy_generation / 1000) * 365

time_interval = input("Enter the desired time interval (D for daily, M for monthly, Y for yearly): ")
while time_interval.upper() not in ['D', 'M', 'Y']:
    print("Invalid input! Please select a valid time interval (D for daily, M for monthly, Y for yearly).")
    time_interval = input("Enter the desired time interval (D for daily, M for monthly, Y for yearly): ")

if time_interval.upper() == 'D':
    energy_generation *= 1   # Daily energy generation
    energy_generation_kwh = energy_generation / 1000
elif time_interval.upper() == 'M':
    energy_generation *= 30  # Monthly energy generation (assuming 30 days in a month)
    energy_generation_kwh = energy_generation / 1000
    time_frame = True
elif time_interval.upper() == 'Y':
    energy_generation *= 365  # Yearly energy generation (assuming 365 days in a year)
    energy_generation_kwh = energy_generation / 1000
    time_frame = True
else:
    print("Invalid input! Please select a valid time interval.")
    time_interval = input("Enter the desired time interval (D for daily, M for monthly, Y for yearly): ")



print(f"Based on the provided inputs and the selected time interval, your solar panel is estimated to generate an energy output of {round(energy_generation_kwh, 2)} kWh")
print(end='\n')


# creating the dataset
data = {'Daily Energy Generation': daily_energy_generation_kWh, 'Monthly Energy Generation': monthly_energy_generation_kWh, 'Yearly Energy Generation': yearly_energy_generation_kWh,}
how_long = list(data.keys())
values = list(data.values())

fig = plt.figure(figsize=(10, 5))

# creating the bar plot
plt.bar(how_long, values, color='cornflowerblue',
        width=0.4)

plt.xlabel("Time Interval")
plt.ylabel("Energy Generation (in kWh)")
plt.title("Solar Panel Energy Generation")


show_graph = input("Type 'show' if you want to see a bar chart of your energy generation at all time intervals (press enter if not): ")
if(show_graph == 'show'):
    plt.show()
    print(end='\n')
    print("Thank you!")
elif(show_graph == ''):
    print(end='\n')
    print("Thank you!")
else:
    print(end='\n')
    print("Thank you!")