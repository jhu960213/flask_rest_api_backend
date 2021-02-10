from flask import Flask
from flask import jsonify
from flask_restful import Api, Resource

app = Flask(__name__)  # flask app instantiation
api = Api(app)  # wrap our flask app in a API (which we are currently using REST api)

# define a dictionary of information to be returned
names_dict = {'jack': {'age': 25, 'gender': 'male'},
              'ben': {'age': 21, 'gender': 'male'}}

# video dict
videos_dict = {}


# creating a resource here, usually a class that inherits the Resource class where we will be able to overwrite
# methods such HTTP GET, PUT, POST, DELETE, etc which will be mapped to our specific HTTP endpoints
# and will later on interact with our database
class MyResource(Resource):

    # HTTP GET request
    @staticmethod
    def get(self, name):
        return jsonify(names_dict[str(name)])

    # HTTP POST request
    @staticmethod
    def post(self):
        return jsonify({'data': "posted!!!"})


# another resource.... for video
class Video(Resource):

    @staticmethod
    def get(self, video_id):
        return videos_dict[video_id]


# adding resources my rest api
# essentially determining what the route is going to be for my added resource
# this is a way to pass params in my http requests "/hello<string:name>/<int:age>"
api.add_resource(MyResource, "/hello/<string:name>")  # in this case the route is "localhost/hello"
api.add_resource(Video, "/video/<int:video_id>") # video end point with 1 param

if __name__ == "__main__":
    app.run(debug=True)  # starts a localhost flask webserver debug is true to help you see the errors if there's any
