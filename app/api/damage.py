# -*- coding: utf-8 -*-
# Coded By Kuduxaaa

from flask import request, jsonify
from flask_restful import Resource
from app.service import predict, detect_damage_part

import os

class DamagePrediction(Resource):
    def get(self):
        """
        Route get method
        type something :)
        happy coding
        """
        
        if 'image' not in request.args or len(request.args['image']) <= 0:
            return {
                'success': False,
                'message': 'required data is missing'
            }
            
        image = request.args.get('image')
        
        if not os.path.exists(os.path.join(os.path.dirname(__file__), '../public/uploads/' + image)):
            return {
                'success': False,
                'message': 'Image not found'
            }
        
        tmp = predict(image)
        
        return detect_damage_part(tmp[0],tmp[1],tmp[2])


    def post(self):
        """
        Route post method
        type something :)
        happy coding
        """

        pass


    def delete(self):
        """
        Route delete method
        type something :)
        happy coding
        """

        pass
