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
        # (City, Country, Temp_celsius, temp_fehrenheit, icon, weather)
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_c = temp_kelvin - 273.15
        temp_f = (temp_kelvin - 273.15) * 9 /5 +32
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        final = (city, country, temp_c, temp_f, icon, weather)
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
    else:
        messagebox.showerror('Error', 'Cannot find city {}'.format(city))



app = Tk()
app.title("Weather app")
app.geometry('700x350')



city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack() #to place it on the screen

search_button=Button(app, text='Search weather', width=12, command=search) #pass search function
search_button.pack() #places it on the screen

location_lbl = Label(app, text='', font=('bold', 20))
location_lbl.pack()

# image = Label(app, bitmap='')
image = Label(app, image='')
image.pack()

temp_lbl = Label(app, text='', font=('bold', 20))
temp_lbl.pack()

weather_lbl = Label(app, text='', font=('bold', 20))
weather_lbl.pack()



app.mainloop()