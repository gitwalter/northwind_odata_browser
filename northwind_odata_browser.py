from flask import Flask, render_template, request
import pyodata
import requests

app = Flask(__name__)

service_url = 'https://services.odata.org/V2/Northwind/Northwind.svc/'
service = pyodata.Client(service_url, requests.Session())

entity_sets = service.schema.entity_sets        
entities = [entity_set.name for entity_set in entity_sets]        

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        entity_name = request.form.get('entity_name')
        # entity_set = service.entity_sets[entity_name]
        entity_set = service.entity_sets._entity_sets.get(entity_name)
        data = entity_set.get_entities().execute()

        entity_properties = list(entity_set._entity_set.entity_type._properties.keys())

        return render_template('index.html', entities=entities, data=data, properties=entity_properties, entity_name=entity_name)
    else:        
        return render_template('index.html', entities=entities)

if __name__ == '__main__':
    app.run()
