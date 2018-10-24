import os
from flask_bootstrap import Bootstrap
from flask import Flask, render_template,abort
import json

app = Flask(__name__)
Bootstrap(app)
app.config["DEBUG"] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def index():
    # 读取文件夹下的所有.json 文件

    dir = r"D:\Python_project\ShiyanlouFlask\files\\"
    listdir = os.listdir(dir)
    list_name = []
    for file in listdir:
        with open(dir + file, "r") as f:
            data = json.load(f)
            list_name.append(data)
    mes = list_name
    return render_template('index.html', data=mes)


@app.route("/files/<filename>")
def file(filename):
    dir = r"D://Python_project//ShiyanlouFlask//files//"
    mes = {}
    if filename + ".json" == "helloshiyanlou.json":
        with open(dir + filename + ".json", "r") as f:
            data = json.load(f)
            mes = data
    elif filename + ".json" == "helloworld.json":
        with open(dir + filename + ".json", "r") as f:
            data = json.load(f)
            mes = data
    else:
        abort(404)
    sendmes = mes
    return render_template('file.html', data=sendmes)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run()
