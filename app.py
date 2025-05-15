from flask import Flask
app =Flask(__name__)


#only if you are not setting the FLASK_APP variable to app.py and using python
if __name__ == '__main__':
    app.run(debug=True)
