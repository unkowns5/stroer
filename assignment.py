from flask import Flask, jsonify, request
from functools import cache
import requests

frank_metrics = {
    'requests': 0,
    'responses': 0,
}

fawa_metrics = {
    'requests': 0,
    'responses': 0,
}

api_frank = 'https://api.frankfurter.dev/v1/latest'
api_fawa = 'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies'
app = Flask(__name__)

@app.route('/exchangeRates/<baseCur>', methods=['GET'])
def get_exchange_rates(baseCur):
    symbols = request.args.get('symbols')
    rates = {}
    
    if not baseCur or not symbols:
        return jsonify({'error': 'Missing required parameters'}), 400
    for sym in symbols.split(','):
        rates[sym] = get_exchange_rates_avg(baseCur, sym)
        
    return jsonify({
        'datasource': 'Free Currency Rates API', 
        'base': baseCur, 
        'rates': rates
    })

@app.route('/metrics', methods=['GET'])
def get_metrics():
    return jsonify({
        'totalQueries': fawa_metrics['requests'],
        'apis': [{
            'name': 'frankfurter',
            'metrics': {
                'totalRequests': frank_metrics['requests'],
                'totalResponses': frank_metrics['responses']
            }
        },
        {
            'name': 'exchangeRatesAPI',
            'metrics': {
                'totalRequests': fawa_metrics['requests'],
                'totalResponses': fawa_metrics['responses']
            }
        }]
    })


@cache
def get_exchange_rates_fawa(baseCur):
    fawa_metrics['requests'] += 1
    try:
        result = requests.get(api_fawa +  '/' + baseCur + '.json')
        result.raise_for_status()
        fawa_metrics['responses'] += 1
        return result.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}, 500
    
@cache
def get_exchange_rates_frank(baseCur, symbols):
    frank_metrics['requests'] += 1
    try:
        result = requests.get(api_frank, params={'base': baseCur, 'symbols': symbols})
        result.raise_for_status()
        frank_metrics['responses'] += 1
        return result.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}, 500

def get_exchange_rates_avg(baseCur, sym):
    fawa = get_exchange_rates_fawa(baseCur.lower()).get(baseCur.lower()).get(sym.lower())
    frank = get_exchange_rates_frank(baseCur, sym).get('rates').get(sym)
    return (fawa + frank) / 2

if __name__ == '__main__':
    app.run()