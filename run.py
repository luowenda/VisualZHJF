#encoding:utf-8


from flask import Flask,render_template
import config
import os
import json

app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/radar')
def radar():
    id = "201611580516"
    with open('data/info.json', encoding='utf-8') as json_file:
	    data = json.load(json_file)
    score = data[id]["score"]
    name = data[id]["name"]
    return render_template('radar.html',score = score,name = name)

@app.route('/zhexian')
def zhexian():
    A_data=[3.17, 3.75, 3.21, 3.46, 3.43, 3.31, 3.08, 3.61]
    B_data=[3.1, 3.00, 3.38, 3.01, 3.52, 3.87, 3.37, 3.85]
    return render_template('zhexian.html',A_data=A_data,B_data=B_data)

if __name__ == '__main__':
    app.run()