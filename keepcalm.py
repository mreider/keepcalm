import os
from flask import Flask, json, render_template, request
import redis
import requests
app = Flask(__name__)
port = int(os.getenv("PORT"))
vcap = json.loads(os.environ['VCAP_SERVICES'])
svc = vcap['rediscloud'][0]['credentials']
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
