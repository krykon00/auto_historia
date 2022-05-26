__author__ = "Koniuszy Krystian"

from flask import Flask
from flask_restful import Api, Resource

from config import Config
from scrapper import CarHistory


app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)

class CarHistoryData(Resource):
    def get(self, plate, vin, date):
        first_regist_date = f'{date[:2]}.{date[2:4]}.{date[4:]}'
        print(plate, vin, first_regist_date)
        data = CarHistory(plate, vin, date)
        return data.get_car_history()
    
    
api.add_resource(CarHistoryData, "/d/<string:plate>/<string:vin>/<string:date>")

if __name__ == "__main__":
    app.run()