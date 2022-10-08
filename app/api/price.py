# -*- coding: utf-8 -*-
# Coded By Kuduxaaa

import json, requests

from flask import request
from flask_restful import Resource
from app.service import PriceCalculator

predictor = PriceCalculator()

# This is example API Resource
class PricePrediction(Resource):
    def get(self):
        """
        Route get method
        type something :)
        happy coding
        """
        
        if 'model' not in request.args or len(request.args['model']) <= 0 and \
            'brand' not in request.args or len(request.args['brand']) <= 0 and \
            'year' not in request.args or len(request.args['year']) <= 0:
                
            return {
                'success': False,
                'message': 'required data is missing'
            }
            
            
        model = request.args.get('model').lower()
        brand = request.args.get('brand').lower()
        year = request.args.get('year').lower()
        
        results = predictor.predict_price(year, brand, model)
        
        if results is not None:
            return {
                'success': True,
                'average': results,
                'message': f'საშუალო ფასი ბაზარზე არის: ${str(results)} 💸'
            }
            
        else:
            return {
                'success': False,
                'message': 'ამ მანქანის ფასები ვერ ვნახეთ 🥺'
            }


    def post(self):
        data = request.form
        
        if not 'brand' in data or len(data['brand']) <= 0 or 'year' not in data:
            return {
                'success': False,
                'message': 'Required data are missing'
            }      
            
        brand = data['brand']
        year = data['year']
        
        url = f'https://api2.myparts.ge/api/ka/products/get?cat_id=1257&limit=15&man_id={brand}&page=1&pr_type_id=1&year_from={year}'
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; en-USD',
            'Accept': 'application/json'
        })
        
        if response.status_code == 200:
            jdata = json.loads(response.text)
            if 'data' in jdata:
                return {
                    'success': True,
                    'price': jdata['data']['products'][0]['price']
                }
        
        return {
            'success': False,
            'message': 'Price not found'
        }


    def delete(self):
        """
        Route delete method
        type something :)
        happy coding
        """

        pass