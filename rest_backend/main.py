from flask import Flask
from flask import jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # flask app instantiation
api = Api(app)  # wrap our flask app in a API (which we are currently using REST api)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # specifies the path of our connected database
db = SQLAlchemy(app)  # fit our flask with with a SQL database


# create our model of our data base
class VideoModel(db.Model):
    # columns of our database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # string can not be null and max at 100 chars
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    # be able to print our our data base
    def __repr__(self):
        return f"Video(name={self.name}, views={self.views}, likes={self.likes})"


# db.create_all()  # creates and initializes the data base. This should only be called ONCE after we specify our
# model!!!

# create a new request parser object so it can help us parse our HTTP request args when invoking our API
req_parser = reqparse.RequestParser()
update_parser = reqparse.RequestParser()

# add arguments to parse for
req_parser.add_argument("name", type=str, help="Please specify a name for the video", required=True)
req_parser.add_argument("likes", type=int, help="Please specify how many likes for the video", required=True)
req_parser.add_argument("views", type=int, help="Please specify how many views for the video", required=True)

# add arguments to updated parser
update_parser.add_argument("name", type=str, help="Please specify a name for the video")
update_parser.add_argument("likes", type=int, help="Please specify how many likes for the video")
update_parser.add_argument("views", type=int, help="Please specify how many views for the video")

# define a dictionary of information to be returned
names_dict = {'jack': {'age': 25, 'gender': 'male'},
              'ben': {'age': 21, 'gender': 'male'}}


# # video dict
# videos_dict = {}


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


# defines how we want instances of our video model to be serialized in JSON objects
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


# another resource.... for video
class Video(Resource):

    # returning an video back to client from data base by serializing following a specific format
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()  # queries by id column returns the first matching case
        if not result:
            abort(404, message="Could not find video with that id...")
        return result

    # can specify a response code along with the sent data, HTTP 201 = data entry has been created
    @marshal_with(resource_fields)
    def put(self, video_id):
        parsed_args = req_parser.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id taken.....")
        video = VideoModel(id=video_id, name=parsed_args['name'],
                           views=parsed_args['views'], likes=parsed_args['likes'])
        db.session.add(video)  # temp add video to data base
        db.session.commit()  # commit the added video to the data base for persistence
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        parsed_args = update_parser.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video does not exist, cannot update....")
        if parsed_args['name']:
            result.name = parsed_args['name']
        if parsed_args['likes']:
            result.likes = parsed_args['likes']
        if parsed_args['views']:
            result.views = parsed_args['views']
        db.session.commit()
        return result

    # # delete an entry in data base, if successful then HTTP 204 = delete successfully
    # def delete(self, video_id):
    #
    #     return deleted, 204

    # # aborting if item already exists HTTP 409 = conflict
    # def _abort_if_exists(self, video_id):
    #     if video_id in videos_dict:
    #         abort(409, message="Video already exists!")
    #
    # # will abort the HTTP request if video id does not exits HTTP 404 = not valid or not found
    # def _abort_if_not_exists(self, video_id):
    #     if video_id not in videos_dict:
    #         abort(404, message="Video id not valid...")


# adding resources my rest api
# essentially determining what the route is going to be for my added resource
# this is a way to pass params in my http requests "/hello<string:name>/<int:age>"
api.add_resource(MyResource, "/hello/<string:name>")  # in this case the route is "localhost/hello"
api.add_resource(Video, "/video/<int:video_id>")  # video end point with 1 param

if __name__ == "__main__":
    app.run(debug=True)  # starts a localhost flask webserver debug is true to help you see the errors if there's any
