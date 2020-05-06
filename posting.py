# Imported modules
import json, datetime
from datetime import datetime
import boto3
from flask import Flask, abort, jsonify, request, g
from flask_dynamo import Dynamo
from boto3.dynamodb.conditions import Key, Attr

app = Flask(__name__)

# DynamoDB table definition for the keys
app.config['DYNAMO_TABLES'] = [
    dict(
        TableName='posts',
        KeySchema=[dict(AttributeName='community', KeyType='HASH'), dict(AttributeName='postID', KeyType='RANGE')],
        AttributeDefinitions=[dict(AttributeName='community', AttributeType='S'), dict(AttributeName='postID', AttributeType='S')],
        ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
    )
]

dynamo = Dynamo(app)

# When the command "flask init" is run, the DynamoDB table is created
@app.cli.command('init')
def init_db():
    # Borrowed from: https://flask-dynamo.readthedocs.io/en/latest/quickstart.html#create-your-tables
    with app.app_context():
        dynamo.create_all()

# Borrowed from: https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

# Home page
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Welcome to the home page of the Reddit Post Microservice.</p>'''

# Create a new post
@app.route('/api/v1.0/resources/collections', methods=['POST'])
def create_post():
    parameters = request.get_json(force=True)

    postID = parameters['postID']
    title = parameters['title']
    text = parameters['text']
    community = parameters['community']
    username = parameters['username']
    currentDateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # If the URL is not provided, there is a total of 5 arguments
    if len(parameters.keys()) == 5:
        # Insert into DynamoDB
        dynamo.tables["posts"].put_item(
            Item = {
                "community": community,
                "postID": str(postID),
                "title": title, 
                "date_time": currentDateTime, 
                "text": text, 
                "username": username, 
            }
        )

    # If the URL is provided, there will be a total of 6 arguments
    elif len(parameters.keys()) == 6:

        url = parameters['url']

        # Insert into DynamoDB
        dynamo.tables["posts"].put_item(
            Item = {
                "community": community,
                "postID": str(postID),
                "title": title, 
                "date_time": currentDateTime, 
                "text": text, 
                "url": url,
                "username": username, 
            }
        )

    location = f"/api/v1.0/resources/collections/{postID}"
    result = {'msg': 'Created Successfully'}
    
    return jsonify(result), 201, {'location': location}

# GET or DELETE post based on community and timestamp
@app.route('/api/v1.0/resources/collections', methods=['GET', 'DELETE'])
def retrieve_post():
    postID = request.args.get('postID')
    community = request.args.get('community')

    # Retrieve an existing post based on postID and community
    if request.method == 'GET':

        try:
            response = dynamo.tables["posts"].get_item(
                ProjectionExpression = "title, community, date_time, username",
                Key = {
                    "postID": postID,
                    "community": community
                }
            )

            # item is already in JSON format
            item = response["Item"]
            return item

        except: 
            result = abort(404, description="Resource not found")
            return jsonify(result)

    # Delete an existing post based on postID and community
    if request.method == 'DELETE':
        try:
            response = dynamo.tables["posts"].get_item(
                Key = {
                    "postID": postID,
                    "community": community
                }
            )

            item = response["Item"]

            if len(item) != 0:
                dynamo.tables["posts"].delete_item(
                    Key = {
                        "postID": postID,
                        "community": community
                    }
                )

                msg = {'msg': 'The post has been deleted'}
                return jsonify(msg)

        except: 
            result = abort(404, description="Resource not found")
            return jsonify(result)

# Retrieve the n most recent posts from a particular community
@app.route('/api/v1.0/resources/collections/recent', methods=['GET'])
def retrieve_community_posts():
    args = request.args.get('community')
    amount = request.args.get('amount')

    response = dynamo.tables["posts"].query(
            ProjectionExpression = "title, community, date_time, username",
            KeyConditionExpression = Key("community").eq(args),
            Limit = int(amount)
    )

    items = response["Items"]

    if len(items) == 0: 
        result = abort(404, description="Resource not found")
        return result

    elif len(items) < int(amount): 
        result = abort(404, description="Resource not found")
        return result


    return jsonify(items)

# Retrieve the n most recent posts from any community
@app.route('/api/v1.0/resources/collections/any', methods=['GET'])
def retrieve_all_posts():
    amount = request.args.get('amount')
    amount = int(amount)-1
    
    response = dynamo.tables["posts"].scan(
        ProjectionExpression = "title, community, date_time, username",
        FilterExpression = Key("postID").between(str(0), str(amount)),
    )
    
    items = response["Items"]

    if len(items) == 0: 
        result = abort(404, description="Resource not found")
        return result

    elif len(items) < int(amount):
        result = abort(404, description="Resource not found")
        return jsonify(result)

    else: 
        return jsonify(items)

if __name__ == '__main__':
    app.run(debug=True)

