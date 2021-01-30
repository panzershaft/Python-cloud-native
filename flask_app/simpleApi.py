from flask import Flask
from flask_restful import Resource, Api
import os

app = Flask(__name__)
api = Api(app)


class createMessage(Resource):
    def get(self):
        return {'message': 'You have received a meesage'}


api.add_resource(createMessage, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3111)))
