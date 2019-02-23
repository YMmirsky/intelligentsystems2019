
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
app.debug = True

@app.route("/", methods=['GET', 'POST'])
# @app.route("/task2", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        name = request.form["name"]
        return name + " Hello"
    return render_template("index.html")

@app.route("/cv_cmd", methods=['GET', 'POST'])
def index2():
    if request.method == "POST":
        name = request.form['dir']
        print 'data from client: ', name
        dictToReturn = {'dir':'ACK'}
        return jsonify(dictToReturn)
    else:
        print 'nodata'
        return jsonify({'dir':'NACK'})        

#    input_json = request.get_json(force=False)
#    print 'data from client: ', input_json
#    dictToReturn = {'dir':'ACK'}
#    return jsonify(dictToReturn)



if __name__ == "__main__":
    app.run()
