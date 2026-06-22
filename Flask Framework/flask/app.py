from flask import Flask, render_template
'''
It creates a instance of the Flask class, 
which will be your WSGI (Web Server Gateway Interface) application.
'''
## WSGI Application
app = Flask(__name__) 

@app.route("/")
def welcome():
    return "<html><body><h1>Welcome to Flask Framework</h1></body></html>"

@app.route("/index")
def welcome_index():
    return render_template("index.html")

@app.route("/about")
def welcome_about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)