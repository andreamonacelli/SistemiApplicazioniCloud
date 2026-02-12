from flask import Flask, render_template_string,render_template, request
from dao import DAO
from genericFormsTemplate import GenericForm  # To be changed with the actual forms file and class
import json
import os
from google.cloud import pubsub_v1

app = Flask(__name__, static_url_path='/static', static_folder='static')

dao = DAO()

topic_name = os.environ['TOPIC'] if 'TOPIC' in os.environ.keys() else 'topic'
project_id = 'exam'
# project_id = os.environ['PROJECT_ID'] if 'PROJECT_ID' in os.environ.keys() else 'exam'
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)


# dictionary to object (pre-prepared)
class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


@app.route('/items', methods=['GET'])
def get_items():
    items = dao.get_items_with_identifier()
    if items is not None:
        return render_template('item_list.html', items=items)
    else:
        return render_template('item_list.html', items=[])


@app.route("/item/<itemid>", methods=['GET', 'POST'])
def get_item(itemid):
    item = dao.get_item(itemid)

    # POST -> add the new item OR update it
    if request.method == 'POST':
        form = GenericForm(request.form)
        if item:
            dao.update_item(itemid, 'new_property')
            item = dao.get_item(itemid)
        else:
            dao.add_item('property')
            item = dao.get_item(itemid)

    # GET -> get the item and display it
    if item is None:
        item = {'propert1': "value", 'property2': "value", '...': 0}
    # Populate form fields with current item data
    form = GenericForm(obj=Struct(**item))

    return render_template('item_with_form.html',  item=item, form=form)


@app.route('/')
def index():
    return render_template('index.html', item=None)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', path=request.path), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080,debug=True)
