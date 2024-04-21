from flask import Flask, render_template, request,send_file
import plotly.graph_objs as go
import  io

app = Flask(__name__)

Lewisuni_coordinates={
    "Romeoville": {
        "latitude": 41.60687051879109,
        "longitude": -88.07983952694718
    },
    "Oak Brook": {
        "latitude": 41.849704827990585,
        "longitude": -87.94512755057589
    },
    "Albuquerque": {
        "latitude": 35.107204505190644,
        "longitude": -106.5675698175947
    },
    "College of DuPage": {
        "latitude": 41.84120967960425,
        "longitude": -88.07337229024918
    },
    "Joliet Junior College": {
        "latitude": 41.51043180472986,
        "longitude": -88.17855687273331
    },
    "Hickory Hills": {
        "latitude": 41.716190756723314,
        "longitude": -87.82041653073465
    },
    "Tinely Park": {
        "latitude": 41.55518054280682,
        "longitude": -87.7934635460868
    },
    "Wiley Delasalle Institute": {
        "latitude": 41.83190967445167,
        "longitude": -87.62348654986252
    }
}


# @app.route('/map', methods=['POST'])
def generate_map(places):
    # Retrieve latitude and longitude data from the request
    traces = []
    for place in places:
        latitude= round(Lewisuni_coordinates[place]['latitude'], 6)
        longitude=round(Lewisuni_coordinates[place]['longitude'], 6)
        print(latitude,longitude)
    # Create a scattermapbox trace
        trace = go.Scattermapbox(
            lat=[latitude],
            lon=[longitude],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=14
            ),
          name=place
        )
        traces.append(trace)
    

    # Create the layout for the map
    layout = go.Layout(
        autosize=True,
        mapbox=dict(
            center=dict(lat=41.60687051879109, lon=-88.07983952694718),
            style='open-street-map',
            zoom=10
        )
    )

    # Create the figure
    fig = go.Figure(data=traces, layout=layout)
    # image_path = 'map_image.png'
    # fig.write_image(image_path, format='png')
    # return None

    plot_div = fig.to_html(full_html=False)
    return plot_div


# generate_map(places=Lewisuni_coordinates.keys())