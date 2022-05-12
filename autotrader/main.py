from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Welcome to the Autotrader prediction api</p>"



if __name__ == '__main__':
    app.run(debug=True)