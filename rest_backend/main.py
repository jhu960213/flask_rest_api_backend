from flask import Flask
from flask import jsonify
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)  # flask app instantiation
api = Api(app)  # wrap our flask app in a API (which we are currently using REST api)

# create a new request parser object so it can help us parse our HTTP request args when invoking our API
req_parser = reqparse.RequestParser()

# add arguments to parse for
req_parser.add_argument("name", type=str, help="Please specify a name for the video", required=True)
req_parser.add_argument("likes", type=int, help="Please specify how many likes for the video", required=True)
req_parser.add_argument("views", type=int, help="Please specify how many views for the video", required=True)

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
    def get(self, name):
        return jsonify(names_dict[str(name)])

    # HTTP POST request
    def post(self):
        return jsonify({'data': "posted!!!"})


# another resource.... for video
class Video(Resource):

    # returning an item back to client
    def get(self, video_id):
        self._abort_if_not_exists(video_id=video_id)
        return videos_dict[video_id]

    # can specify a response code along with the sent data, HTTP 201 = data entry has been created
    def put(self, video_id):
        self._abort_if_exists(video_id=video_id)
        parsed_args = req_parser.parse_args()
        videos_dict[video_id] = parsed_args
        return videos_dict[video_id], 201

    # delete an entry in data base, if successful then HTTP 204 = delete successfully
    def delete(self, video_id):
        self._abort_if_not_exists(video_id=video_id)
        deleted = videos_dict[video_id]
        del videos_dict[video_id]
        return deleted, 204

    # aborting if item already exists HTTP 409 = conflict
    def _abort_if_exists(self, video_id):
        if video_id in videos_dict:
            abort(409, message="Video already exists!")

    # will abort the HTTP request if video id does not exits HTTP 404 = not valid or not found
    def _abort_if_not_exists(self, video_id):
        if video_id not in videos_dict:
            abort(404, message="Video id not valid...")



# adding resources my rest api
# essentially determining what the route is going to be for my added resource
# this is a way to pass params in my http requests "/hello<string:name>/<int:age>"
api.add_resource(MyResource, "/hello/<string:name>")  # in this case the route is "localhost/hello"
api.add_resource(Video, "/video/<int:video_id>")  # video end point with 1 param

if __name__ == "__main__":
    app.run(debug=True)  # starts a localhost flask webserver debug is true to help you see the errors if there's any
