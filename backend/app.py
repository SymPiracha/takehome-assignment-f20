from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db
import json

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)

# PART 3
@app.route("/shows", methods=['GET', 'POST'])
def shows():
    # GET Request
    if request.method == 'GET':
        return create_response({"shows": db.get('shows')})
    # POST Request
    if request.method == 'POST':
        # Access data you get from post request and store it in variables
        data_json = request.get_data()
        data = json.loads(data_json)
        
        data_name =  data['name']
        data_episodes_seen = data['episodes_seen']
        if data_name != "" or data_episodes_seen >= 0:
            # add it to the database
            db.create('shows', data)
            # get the list of shows
            list_of_shows = db.get('shows')
            #find out size of list and get id of show just added
            size_of_list = len(list_of_shows)
            id_number_of_show_added =  list_of_shows[size_of_list-1]['id']
            #display the show that has been added with status code 201
            return create_response({"shows": db.get('shows')[int(id_number_of_show_added)-1]}, status=201)

        else:
            return create_response(status=422, message="Error, make sure you include name and episodes seen of the TV show")
       
        
        


@app.route("/shows/<id>", methods=['GET', 'DELETE', 'PUT'])
def show_with_id(id):
    # PART 2
    if request.method == 'GET':
        if db.getById('shows', int(id)) is None:
            return create_response(status=404, message="No show with this id exists")
        return create_response({"shows": db.get('shows')[int(id)-1]})
    if request.method == 'DELETE':
        if db.getById('shows', int(id)) is None:
            return create_response(status=404, message="No show with this id exists")
        db.deleteById('shows', int(id))
        return create_response(message="Show deleted")
    # PART 4
    if request.method == 'PUT':
        if db.getById('shows', int(id)) is None:
            return create_response(status=404, message="No show with this id exists")
        else: 
            # store values recevied in corresponding variables
            data_json = request.get_data()
            data = json.loads(data_json)
        
            
            # if name and episodes are not provided, keep orignal values
            if data['name'] == "":
                data['name'] = db.getById('shows', int(id))['name']
            if data['episodes_seen'] == "":
                data['episodes_seen'] = db.getById('shows', int(id))['episodes_seen']
                
            # update show with corresponding ID
            db.updateById('shows', int(id), data)
            # return results
            return create_response({"shows": db.get('shows')[int(id)-1]}, status=201)
            





"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(port=8080, debug=True)
