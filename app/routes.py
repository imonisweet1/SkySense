from flask import render_template, request, jsonify
from app import app, db
from app.models import User, Preferences
import requests
import os

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather/current', methods=['GET'])
def current_weather():
    location = request.args.get('location')
    api_key = os.getenv('WEATHER_API_KEY')
    response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}')
    return jsonify(response.json())

@app.route('/weather/forecast', methods=['GET'])
def weather_forecast():
    location = request.args.get('location')
    api_key = os.getenv('WEATHER_API_KEY')
    response = requests.get(f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=7')
    return jsonify(response.json())

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
        return jsonify({'location': preference.location})
    return jsonify({'message': 'User not found'}), 404
