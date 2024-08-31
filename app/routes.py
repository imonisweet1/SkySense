from flask import render_template, request, jsonify
from app import app, db
from app.models import User, Preferences
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch the API key from the environment variables
API_KEY = os.getenv('WEATHER_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather/current', methods=['GET'])
def current_weather():
    location = request.args.get('location')
    if not location:
        return jsonify({'error': 'Location is required'}), 400

    # Make a request to the weather API using the loaded API key
    response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}')
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to fetch weather data'}), response.status_code

@app.route('/weather/forecast', methods=['GET'])
def weather_forecast():
    location = request.args.get('location')
    if not location:
        return jsonify({'error': 'Location is required'}), 400

    # Make a request to the weather API for the forecast
    response = requests.get(f'http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location}&days=7')
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to fetch weather data'}), response.status_code

@app.route('/user/preferences', methods=['POST'])
def save_preferences():
    user_id = request.form.get('user_id')
    location = request.form.get('location')
    user = User.query.get(user_id)
    if user:
        preference = Preferences(location=location, user=user)
        db.session.add(preference)
        db.session.commit()
        return jsonify({'message': 'Preferences saved successfully!'})
    return jsonify({'message': 'User not found'}), 404

@app.route('/user/preferences', methods=['GET'])
def get_preferences():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    if user:
        preference = Preferences.query.filter_by(user_id=user_id).first()
        if preference:
            return jsonify({'location': preference.location})
        else:
            return jsonify({'message': 'Preferences not found'}), 404
    return jsonify({'message': 'User not found'}), 404
