from flask import Flask, render_template, request, redirect, url_for

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

@app.route("/submit", methods=["GET", "POST"])
def submit_page():
    if request.method == "POST":
        name = request.form['name']
        return f"Hello {name}, welcome to Flask Framework!"
    return render_template("form.html")

# Building URL Dynamically
@app.route('/success/<int:score>')
def success_page(score):
    res = "PASS" if score >= 50 else "FAIL"
    return render_template("result.html", result=res)

@app.route('/successres/<int:score>')
def successres_page(score):
    res = "PASS" if score >= 50 else "FAIL"
    exp = {'score': score, "res": res}
    return render_template("result1.html", results=exp)

# if condition in template
@app.route('/successif/<int:score>')
def successif(score):
    return render_template("result.html", result=score)

@app.route('/fail/<int:score>')
def fail(score):
    return render_template("result.html", result=score)

@app.route('/submit1', methods=["GET","POST"])
def submit_scores():
    if request.method == 'POST':
        science = float(request.form['science'])
        maths = float(request.form['maths'])   # matches HTML field name
        c = float(request.form['c'])
        datascience = float(request.form['datascience'])  # matches HTML field name
        total_score = science + maths + c + datascience

        return redirect(url_for('successres_page', score=int(total_score)))

    return render_template("getresult.html")  # show the form again if GET

if __name__ == '__main__':
    app.run(debug=True)