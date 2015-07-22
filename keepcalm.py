import os
from flask import Flask, json, render_template, request
import redis
import requests
app = Flask(__name__)
port = int(os.getenv("PORT"))
vcap = json.loads(os.environ['VCAP_SERVICES'])

# for a local CF (not pivotol web services) change this next bit to svc = vcap['p-redis'][0]['credentials']
svc = vcap['rediscloud'][0]['credentials']

# for a local CF (not pivotal web services) change this next bit to
# db = redis.StrictRedis(host=svc["host"], port=svc["port"], password=svc["password"],db=0)
db = redis.StrictRedis(host=svc["hostname"], port=svc["port"], password=svc["password"],db=0)

@app.route('/update',methods=["POST"])
def update():
    message = request.form["message"]
    db.set('message',message)
    return json.dumps({'message':'success'})

@app.route('/message')
def message():
    message = db.get('message')
    return render_template('message.html', message=message)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
