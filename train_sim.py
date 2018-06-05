import os
from sqlalchemy import exc
# import requests
from flask import (
    Flask,
    request,
    abort,
    url_for,
    redirect,
    session,
    render_template,
    flash
)

from flask_restful import (
    reqparse,
    abort,
    Api,
    Resource
)

from models import (
    db,
    Block,
    Station,
    Switch,
    Crossing,
    Light,
    Train
)

from resources import (
    BlockResource,
    BlockListResource,
    StationResource,
    StationListResource,
    SwitchResource,
    SwitchListResource,
    CrossingResource,
    CrossingListResource,
    LightResource,
    LightListResource,
    TrainResource,
    TrainListResource,
    MessageResource
)

app = Flask(__name__)
app.static_folder = 'static'
api = Api(app)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'train_sim.db')
))

db.init_app(app)

api.add_resource(BlockListResource, '/blocks/')
api.add_resource(BlockResource, '/blocks/<int:id>')
api.add_resource(StationListResource, '/stations/')
api.add_resource(StationResource, '/stations/<string:name>')
api.add_resource(SwitchListResource, '/switches/')
api.add_resource(SwitchResource, '/switches/<int:id>')
api.add_resource(CrossingListResource, '/crossings/')
api.add_resource(CrossingResource, '/crossings/<int:id>')
api.add_resource(LightListResource, '/lights/')
api.add_resource(LightResource, '/lights/<int:id>')
api.add_resource(TrainListResource, '/trains/')
api.add_resource(TrainResource, '/trains/<int:id>')
# api.add_resource(MessageListResource, '/messages/')
api.add_resource(MessageResource, '/messages/<int:id>')

@app.cli.command('initdb')
def initdb_command():
    db.drop_all()
    db.create_all()

    # TODO:
    #   - Parse database file
    #   - Create blocks based on file lines
    #   - Add stations, switches, crossings, lights when appropriate

    print('Initialized the database.')

@app.cli.command('testdb')
def testdb_command():
    db.drop_all()
    db.create_all()

    block1 = Block(id=1,number=1,line="green",length=100.0,grade=0.5,speedLimit=55,elevation=0.5,cumulative_elevation=0.5,occupancy=False)
    db.session.add(block1)

    block2 = Block(id=2,number=2,line="green",length=100.0,grade=1.0,speedLimit=55,elevation=1.0,cumulative_elevation=1.5,occupancy=True)
    db.session.add(block2)

    block3 = Block(id=3,number=3,line="green",length=100.0,grade=1.5,speedLimit=55,elevation=1.5,cumulative_elevation=3.0,occupancy=False)
    db.session.add(block3)

    switch1 = Switch(id=1,state=False)
    db.session.add(switch1)
    block1.switch = switch1

    crossing1 = Crossing(id=1,state=False)
    db.session.add(crossing1)
    block3.crossing = crossing1

    station1 = Station(id=1,name="Station 1")
    db.session.add(station1)
    block2.station = station1

    light1 = Light(id=1,state=False)
    db.session.add(light1)
    light2 = Light(id=2,state=False)
    db.session.add(light1)

    switch1.lights.append(light1)
    switch1.lights.append(light2)

    block1.message = "hello"

    train1 = Train(id=1,name="train1",length=1000.0,width=100.0,height=100.0,mass=1000.0,crewCount=0,passengerCount=0)
    db.session.add(train1)
    train1.front_block_id = block1.id

    db.session.commit()

    # user1 = User(username='user1', password='pass')
    # db.session.add(user1)
    #
    # chatroom1 = ChatRoom(name='Super Awesome Chat Room')
    # db.session.add(chatroom1)
    #
    # user1.created_rooms.append(chatroom1)
    #
    # message1 = Message(creator=user1.username,text="Hello, there!", chatroom=chatroom1.name)
    # db.session.add(message1)
    # db.session.commit()

    print('Initialized the testing database.')

#--------------------------------------------------------------------------------------------

# Home page:
# GET - Visit home page
@app.route("/", methods=['GET'])
def default():
    blocks = Block.query.all()
    ids = [block.id for block in blocks]
    return render_template("home.html", block_ids=ids)

#--------------------------------------------------------------------------------------------

# CTC page:
@app.route("/ctc/", methods=['GET'])
def ctc():
    return render_template("ctc.html")

#--------------------------------------------------------------------------------------------

# Track model page:
@app.route("/track_model/", methods=['GET'])
def track_model():
    blocks = Block.query.all()
    ids = [block.id for block in blocks]
    return render_template("track_model.html", block_ids=ids)

#--------------------------------------------------------------------------------------------

# Track controller page:
@app.route("/track_controller/", methods=['GET'])
def track_controller():
    return render_template("track_controller.html")

#--------------------------------------------------------------------------------------------

# Train model page:
@app.route("/train_model/", methods=['GET'])
def train_model():
    return render_template("train_model.html")

#--------------------------------------------------------------------------------------------

# Train controller page:
@app.route("/train_controller/", methods=['GET'])
def train_controller():
    return render_template("train_controller.html")

#--------------------------------------------------------------------------------------------


if __name__ == "__main__":
	app.run(debug=True)
