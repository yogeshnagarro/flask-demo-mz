import os
from flask import Flask, render_template, url_for, json, request
from datetime import datetime
import urllib.request,numpy,pickle

app = Flask(__name__)
companyName = "Green Energy Forcast"


@app.route("/", methods = ['POST', 'GET'])
def home():
    form_data = {"Lat" : request.form.get("Latitude")}
    data = {}
    Lat = 0
    Long = 0
    city = ''
    # print(form_data.get('Lat'))
    if form_data.get('Lat'):
        ll = form_data.get('Lat').split(',')
        # print(ll)
        Lat = float(ll[0])
        Long = float(ll[1])
        if request.method == 'POST':
          data= get_data(Lat,Long)
          
          if data['city']:
              city = data['city']['name']
              print(city)
          data = data["list"]
          wpf_model = pickle.load(open('wpf.pkl','rb'))
          # print(wpf_model.predict(numpy.array([[325,8.43]])))
          for x in data:
              # print(x['wind']['deg'],x['wind']['speed'])
              # print(wpf_model.predict(numpy.array([[x['wind']['deg'],x['wind']['speed']]])))
              a = float(wpf_model.predict(numpy.array([[x['wind']['deg'],x['wind']['speed']]])))
              x['power_avg']= round(a,2)
    
    
    # data = json.load(
    #     open(os.path.join(app.static_folder, 'data/wind-data.json')))
    
    columns = [
        # {
        #     "field": "id",  # which is the field's name of data key
        #     "title": "Row ID",  # display as the table header's name
        #     "sortable": True,
        # },
        # {
        #     "field": "date-time",  # which is the field's name of data key
        #     "title": "Date / Time",  # display as the table header's name
        #     "sortable": True,
        # },
        # {
        #     "field": "wind-speed",  # which is the field's name of data key
        #     # display as the table header's name
        #     "title": "Wind Speed (in m/s)",
        #     "sortable": True,
        # }, {
        #     "field": "wind-direction",  # which is the field's name of data key
        #     # display as the table header's name
        #     "title": "Wind Direction(*)",
        #     "sortable": True,
        # }, {
        #     "field": "power-avg",  # which is the field's name of data key
        #     "title": "Power Avg",  # display as the table header's name
        #     "sortable": True,
        # }
        
        {
            "field": "dt_txt",  # which is the field's name of data key
            "title": "Date / Time",  # display as the table header's name
            "sortable": True,
        },
        {
            "field": "wind.speed",  # which is the field's name of data key
            # display as the table header's name
            "title": "Wind Speed (m/s)",
            "sortable": True,
        },
        {
            "field": "wind.deg",  # which is the field's name of data key
            # display as the table header's name
            "title": "Wind Direction (&deg;)",
            "sortable": True,
        },
        {
            "field": "main.temp",  # which is the field's name of data key
            # display as the table header's name
            "title": "Temperature (&deg;C)",
            "sortable": True,
        },
        {
            "field": "main.humidity",  # which is the field's name of data key
            # display as the table header's name
            "title": "Humidity (%)",
            "sortable": True,
        },
        {
            "field": "power_avg",  # which is the field's name of data key
            "title": "Power Avg",  # display as the table header's name
            "sortable": True,
        }
    ]

    return render_template(
        "data-table.html",
        users=data,
        columns=columns,
        companyName=companyName,
        lat = Lat,
        long = Long,
        city_ = city
    )


@app.route("/api/data")
def get_data(Latitude = 0,Longitude=0):
    url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid=37d73035b107a29659dac1d0276d4d75&units=metric".format(Latitude,Longitude)
    # print(url)
    response = urllib.request.urlopen(url)
    data = response.read()
    return json.loads(data)
    # return app.send_static_file("data.json")

# New functions


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/contact/")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
    # app.run(debug=True,host='0.0.0.0',port=80)
