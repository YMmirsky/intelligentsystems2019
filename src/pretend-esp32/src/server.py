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

@app.route("/task1", methods=['GET', 'POST'])
def index2():
    input_json = request.get_json(force=False)
    print 'data from client: ', input_json
    dictToReturn = {'answer':42}
    return jsonify(dictToReturn)

if __name__ == "__main__":
    app.run()

