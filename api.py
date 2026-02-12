import os
import json
from flask import Flask, request
from flask_restful import Resource, Api
from google.cloud import pubsub_v1
from dao import DAO

app = Flask(__name__, static_url_path='/static', static_folder='static')
api = Api(app)
dao = DAO()
basePath = '/api/v1'

# PubSub stuff
project_id = 'exam'
topic_name = os.environ['TOPIC'] if 'TOPIC' in os.environ.keys() else 'exam_topic'
topic_name2 = os.environ['TOPIC2'] if 'TOPIC2' in os.environ.keys() else 'exam_topic_2'
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)
topic_path2 = publisher.topic_path(project_id, topic_name2)
# publisher.publish(topic_path2, json.dumps(data).encode('utf-8'))


# REMEMBER TO CHANGE THE RESPONSE CODES ACCORDING TO THE EXAM PAPER


class ItemResource(Resource):
    def get(self, itemid):
        item = dao.get_item(itemid)
        if item is None:
            return None, 404
        else:
            return item, 200

    def post(self):
        item_data = request.json
        # Data validation
        if not self.validate_item_data(item_data):
            return None, 400
        # Duplicate check
        item = dao.get_item(item_data['id'])  # Careful: the id key might be different, always refer to the specifics
        if item is not None:
            return item, 409
        dao.add_item('property')
        item = dao.get_item(item_data['id'])
        return item, 201

    def put(self, itemid):
        item_data = request.json
        # Check if item exists (cannot update a non-existing item)
        item = dao.get_item(itemid)
        if item is None:
            return None, 404
        # Validate input data
        if not self.validate_item_data(item_data):
            return None, 400
        dao.update_item(itemid, item_data)  # During the exam fix both the method and its call accordingly to the specifics
        item = dao.get_item(itemid)
        return item, 201

    def delete(self, itemid):
        item = dao.get_item(itemid)
        if item is None:
            return item, 404
        dao.delete_item(itemid)
        return None, 200

    def validate_item_data(self, item_data):
        # Perform data validation according to the specifics
        pass

class CleanResource(Resource):
    def post(self):
        dao.clean_db()
        return None, 200


api.add_resource(ItemResource, f'{basePath}/item/<int:iditem>')
api.add_resource(CleanResource, f'{basePath}/clean')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
