from flask import Flask, render_template, request
'''
It creates an instance of the Flask class, 
which will be your WSGI (Web Server Gateway Interface) application.
'''
## WSGI Application
app = Flask(__name__) 

@app.route("/")
def welcome():
    return "<html><body><h1>Welcome to Flask Framework</h1></body></html>"

@app.route("/index", methods=["GET"])
def welcome_index(): 
    return render_template("index.html")

@app.route("/about")
def welcome_about():
    return render_template("about.html")

@app.route("/form", methods=["GET", "POST"])
def form_page():
    if request.method == "POST":
        name = request.form['name']
        return f"Hello {name}, welcome to Flask Framework!"
    return render_template("form.html")

@app.route("/submit", methods=["GET", "POST"])
def submit_page():
    if request.method == "POST":
        name = request.form['name']
        return f"Hello {name}, welcome to Flask Framework!"
    return render_template("form.html")

if __name__ == '__main__':
    app.run(debug=True)
