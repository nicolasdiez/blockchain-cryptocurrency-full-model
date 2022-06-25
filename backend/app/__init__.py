from flask import Flask

# Create Flask web server
app = Flask(__name__)


# 1st endpoint -> return string 'Test'
@app.route("/")
def default():
    return 'Welcome to the Blockchain!'


# run the Flask web server
app.run()
