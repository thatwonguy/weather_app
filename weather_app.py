from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser #parses the config file
import requests

url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        # (City, Country, Temp_celsius, temp_fehrenheit, icon, weather, lat, lon)
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_c = temp_kelvin - 273.15
        temp_f = (temp_kelvin - 273.15) * 9 /5 +32
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        lat = json['coord']['lat']
        long = json['coord']['lon']
        final = (city, country, temp_c, temp_f, icon, weather, lat, long)
        return final

    else:
        return None

# print(get_weather('London')) #testing results

def search():
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        location_lbl['text'] = '{}, {}'.format(weather[0], weather[1])
        # image['image'] = 'icons/{}.png'.format(weather[4])
        icon_ref = PhotoImage(file='icons/{}.png'.format(weather[4]))
        image['image'] = icon_ref
        image.image = icon_ref 
        temp_lbl['text'] = '{:.2f}°C, {:.2f}°F'.format(weather[2], weather[3]) #limits to 2 decimal places
        weather_lbl['text'] = weather[5]
        lat_lbl['text']=weather[6]
        long_lbl['text']=weather[7]
    else:
        messagebox.showerror('Error', 'Cannot find city {}'.format(city))

def reset_values():
    location_lbl.config(text='Location')
    image.config(text='Weather Image')
    temp_lbl.config(text='Current Temp')
    weather_lbl.config(text='Current Weather')
    lat_lbl.config(text='Latitude')
    long_lbl.config(text='Longitude')


app = Tk()
app.title("Weather app")
app.geometry('700x400')


city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack() #to place it on the screen

search_button=Button(app, text='Search weather', width=12, command=search) #pass search function
search_button.pack() #places it on the screen

reset_button=Button(app, text='Clear', command=reset_values)
reset_button.pack()

location_lbl = Label(app, text='Location', font=('bold', 20))
location_lbl.pack()

# image = Label(app, bitmap='')
image = Label(app, image='', text= 'Weather Image', font=('bold', 20))
image.pack()

temp_lbl = Label(app, text='Current Temperature', font=('bold', 20))
temp_lbl.pack()

weather_lbl = Label(app, text='Current Weather Condition', font=('bold', 20))
weather_lbl.pack()

lat_lbl = Label(app, text='Latitude', font=('bold', 20))
lat_lbl.pack()

long_lbl = Label(app, text='Longitude', font=('bold', 20))
long_lbl.pack()


app.mainloop()