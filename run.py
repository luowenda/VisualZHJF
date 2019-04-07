#encoding:utf-8


from flask import Flask,render_template
import config
import os
import json

app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def test():
    id = "201611580516"
    with open('data/info.json', encoding='utf-8') as json_file:
	    data = json.load(json_file)
    score = data[id]["score"]
    name = data[id]["name"]

    return render_template('index.html',score = score,name = name)

if __name__ == '__main__':
    app.run()