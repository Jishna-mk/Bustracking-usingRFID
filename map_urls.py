from flask import Flask, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from wtforms import StringField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import backref
from flask_socketio import SocketIO
import pandas as pd
import requests
from io import StringIO
import threading
import time
socketio = SocketIO()
# Map URLs for different locations
map_urls = {
    "Kozhikode": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3913.032745915477!2d75.7863465!3d11.259001399999999!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3ba659487cbd1df5%3A0x9d643c0d1e16a77!2sMofussil%20Bus%20Stand%20Building%2C%20Mavoor%20Rd%2C%20New%20Bus%20Stand%2C%20EMS%20Stadium%2C%20Arayidathupalam%2C%20Kozhikode%2C%20Kerala%20673004!5e0!3m2!1sen!2sin!4v1705594927061!5m2!1sen!2sin",
    "Ramanattukara": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3914.130058915313!2d75.86250407481107!3d11.178004888996254!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3ba65070a8949e57%3A0xbac67794705793a4!2sRamanattukara%20Bus%20Stand!5e0!3m2!1sen!2sin!4v1705595168906!5m2!1sen!2sin",
    "Parappanangadi": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3915.868224874814!2d75.85741597480911!3d11.048505189117254!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3ba653869bb42a1b%3A0xa6949885f71180fc!2sParappanangadi%20Bus%20Stand!5e0!3m2!1sen!2sin!4v1705595253445!5m2!1sen!2sin",
    "Valanchery": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1958.986409157789!2d76.07023028853816!3d10.88967019731652!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3ba7b63265ae544b%3A0xe386529d12fcd1b!2sValanchery%20Bus%20Stand!5e0!3m2!1sen!2sin!4v1705595292432!5m2!1sen!2sin"
    # Add similar entries for other locations
}


@socketio.on('update_data')
def handle_update():
    # Fetch the latest data from the CSV file
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQzn2jcm7P_7VLaJIh7gPnkyYj5S6Q161p8DG71GsiR7nGjfiHXxzW9-wftxfZyhizT1xGwFD1E1uGl/pub?output=csv"
    response = requests.get(csv_url)
    csv_data = response.text
    df = pd.read_csv(StringIO(csv_data))

    # Iterate over each row in the DataFrame and emit data to connected clients
    for index, row in df.iterrows():
        location_data = row['name']
        map_url = map_urls.get(location_data, '')
        socketio.emit('update_table', {'table_html': row.to_frame().T.to_html(classes="table table-bordered", index=False)})
        socketio.emit('update_location', {'map_url': map_url, 'location_data': location_data})