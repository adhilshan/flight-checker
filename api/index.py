from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

@app.route('/api/flight-data', methods=['GET'])
def get_flight_data():
    try:
        airline_code = request.args.get('airlineCode')
        flight_number = request.args.get('flightNumber')

        if not airline_code or not flight_number:
            return jsonify({
                'error': 'Airline code and flight number are required'
            }), 400

        # Headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://www.flightstats.com',
            'Referer': 'https://www.flightstats.com/',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }

        # Make request to FlightStats
        url = f'https://www.flightstats.com/v2/api-next/flight-tracker/other-days/{airline_code}/{flight_number}'
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({
                'error': f'Failed to fetch flight data. Status code: {response.status_code}',
                'details': response.text
            }), response.status_code

    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500
