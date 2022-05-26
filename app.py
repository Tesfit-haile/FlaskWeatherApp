import requests
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
# from requests.api import request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

# create DB
db = SQLAlchemy(app)


# create table
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    ################@######### The api key below need to be updated in time in order to work properly ##################
    ###  https://home.openweathermap.org/api_keys ####

    key_code = '6d483ab5a1587192bc4e1975712cec5a'

    if request.method == 'POST':
        # get the city from the input
        input_value = request.form.get('city_name')
        new_city = City(name=input_value)  # add to DB
        city_from_db = City.query.filter_by(name=input_value).first()

        if new_city and city_from_db is None:  # check if city not exist
            db.session.add(new_city)
            db.session.commit()

    list_of_cities = []
    all_cities = City.query.all()

    for city in all_cities:

        ################@######### The api key below need to be updated in time in order to work properly ##################
        ###  https://home.openweathermap.org/api_keys ####

        url = f'http://api.openweathermap.org/data/2.5/weather?q={city.name}&units=imperial&appid={key_code}'
        r = requests.get(url).json()  # will give u cod 200 or 400

        # Celsius = (Fahrenheit – 32) * 5/9
        # Fahrenheit = (Celsius * 9/5) + 32

        if r['cod'] == 200:  # meaning if city exist
            weather_obj_list = {
                'city': r['name'],
                'temperature': round(int((r['main']['temp'] - 32) * 5/9)),
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon'],
            }

            list_of_cities.append(weather_obj_list)

    return render_template('weather.html', list_of_cities=list_of_cities)


@app.route('/delete_all')
def delete_all():
    all_city = City.query.all()
    for city in all_city:
        db.session.delete(city)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
