import json
import requests

from bs4 import BeautifulSoup


class PriceCalculator:    
    def __init__(self):
        self.version = 1.0
        self.base_url = 'https://api2.myauto.ge/ka/{}'
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'
        })


    def __repr__(self):
        return f'<MyAuto v{self.version}>'
    
    
    
    """
    Calculate average price from prices array
    """
    def calculate_average(self, amounts: list) -> int:
        return int(float(sum(amounts)) / max(len(amounts), 1))





    """
    Get car price from car object
    """
    def get_car_price(self, car_item: dict, currency='USD') -> int:
        price_key = 'price_usd' if currency == 'USD' else 'price_value'
        return car_item[price_key] if price_key in car_item and str(car_item[price_key]) != '0' else None




    """
    Final function to predict average price
    """
    def predict_price(self, year, brand, model):
        cars = self.search(year, brand, model)
        prices = self.get_from_ss(model)

        for car in cars:
            price = self.get_car_price(car)
            if price is not None:
                prices.append(price)

        if len(prices) > 2:
            return self.calculate_average(prices)

        return None




    """
    Search in primary provider
    """
    def search(self, year, brand, model):
        page = 1
        response = self.session.get(
            url=self.base_url.format('products'),
            params={
                'TypeID': '0',
                'ForRent': '0',
                'Mans': f'{brand}',
                'ProdYearFrom': str(year),
                'ProdYearTo': str(year),
                'CurrencyID': '3',
                'MileageType': '1',
                'Page': str(page),
                'Keyword': model
            }
        )
        
        if response.status_code == 200:
            data = json.loads(response.content)
            if data.get('statusMessage') == 'statusSuccess':
                items = data.get('data')['items'] or []

                if len(items) <= 0:
                    return []

                return items

        else:
            return []



    """
    Getting car prices from external service
    """

    def get_from_ss(self, car_name: str) -> list:
        response = self.session.get(
            url='https://ss.ge/ka/auto/list/iyideba',
            params={'AutoManufacturerId': '', 'VehicleModelIds': '', 'VehicleDealTypes': '2', 'YearFrom': '', 'YearTo': '', 'CurrencyId': '1', 'PriceFrom': '', 'PriceTo': '', 'CityIds': '', 'Query': car_name, 'MillageFrom': '', 'MillageTo': '', 'EngineFrom': '', 'EngineTo': '', 'IsCustomsCleared': '', 'TechnicalInspection': '', 'AutoDealershipId': '', 'El_Windows': 'false', 'Hatch': 'false', 'CruiseControl': 'false', 'StartStopSystem': 'false', 'AUX': 'false',
                    'Bluetooth': 'false', 'AntiFogHeadlights': 'false', 'SeatHeater': 'false', 'SmartSeats': 'false', 'MultiWheel': 'false', 'Signalisation': 'false', 'BoardComputer': 'false', 'Conditioner': 'false', 'ClimateControl': 'false', 'RearViewCamera': 'false', 'Monitor': 'false', 'PanoramicCeiling': 'false', 'ParkingControl': 'false', 'ABS': 'false', 'CentralLocker': 'false', 'AutoParking': 'false', 'LedHeadlights': 'false', 'AdaptedForDisabled': 'false'}
        )
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find('div', {'class': 'auto-result'})
        
        if results is not None:
            price_divs = results.findAll('div', {'class': 'price priceUsd'})
            if len(price_divs) > 0:
                return [
                    int(price.text.replace(' ', '').strip()) 
                    for price in price_divs
                ]

        return []
