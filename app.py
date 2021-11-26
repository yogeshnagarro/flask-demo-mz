import os
from flask import Flask, render_template, url_for, json, request
import urllib.request, numpy, pickle

app = Flask(__name__)
companyName = "Green Energy Forcast"


@app.route("/", methods = ['POST', 'GET'])
def home():
    form_data = {"Lat" : request.form.get("Latitude")}
    data = {}
    Lat = 0
    Long = 0
    city = ''
    if form_data.get('Lat'):
        ll = form_data.get('Lat').split(',')
        Lat = float(ll[0])
        Long = float(ll[1])
        if request.method == 'POST':
          data= get_data(Lat,Long)
          
          if data['city']:
              city = data['city']['name']
          data = data["list"]

          wpf_model = pickle.load(open('wpf.pkl','rb'))
          for j in data:
            print(j['wind']['deg'],j['wind']['speed'])
          
          for x in data:
              arrm = numpy.array([[x['wind']['deg'],x['wind']['speed']]])
              prdt = wpf_model.predict(arrm)
              a = float(prdt)
              x['power_avg']= round(a,2)
    
    
    # data = json.load(
    #     open(os.path.join(app.static_folder, 'data/wind-data.json')))
    
    columns = [
        {
            "field": "dt_txt",  # which is the field's name of data key
            "title": "Date / Time",  # display as the table header's name
            "sortable": True,
        },
        {
            "field": "wind.speed",  # which is the field's name of data key
            # display as the table header's name
            "title": "Wind Speed (in m/s)",
            "sortable": True,
        },
        {
            "field": "wind.deg",  # which is the field's name of data key
            # display as the table header's name
            "title": "Wind Direction(&deg;)",
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
    url = "http://localhost:3800/forecast/data?lat={}&lon={}&appid=37d73035b107a29659dac1d0276d4d75".format(Latitude,Longitude)
    print(url)
    response = urllib.request.urlopen(url)
    data = response.read()
    return json.loads(data)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
