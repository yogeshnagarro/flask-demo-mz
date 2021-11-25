import os
from flask import Flask, render_template, url_for, json, request
from datetime import datetime

app = Flask(__name__)
companyName = "Green Energy Forcast"

@app.route("/")
def index():
    return "Connected ...."

@app.route("/home", methods = ['POST', 'GET'])
def home():
    form_data = {"Lat" : request.form.get("Latitude"),
    "Log":request.form.get("Longitude")}
    if request.method == 'POST':
      print("form data: ", form_data.get("Lat"));
    
    data = json.load(
        open(os.path.join(app.static_folder, 'data/wind-data.json')))
    columns = [
        {
            "field": "id",  # which is the field's name of data key
            "title": "Row ID",  # display as the table header's name
            "sortable": True,
        }, {
            "field": "date-time",  # which is the field's name of data key
            "title": "Date / Time",  # display as the table header's name
            "sortable": True,
        },
        {
            "field": "wind-speed",  # which is the field's name of data key
            # display as the table header's name
            "title": "Wind Speed (in m/s)",
            "sortable": True,
        }, {
            "field": "wind-direction",  # which is the field's name of data key
            # display as the table header's name
            "title": "Wind Direction(*)",
            "sortable": True,
        }, {
            "field": "power-avg",  # which is the field's name of data key
            "title": "Power Avg",  # display as the table header's name
            "sortable": True,
        }
    ]

    return render_template(
        "data-table.html",
        users=data,
        columns=columns,
        companyName=companyName
    )


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
