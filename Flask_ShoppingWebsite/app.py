from flask import Flask, render_template, request, redirect, session
import sqlite3


app = Flask(__name__)
app.secret_key = "PopoSnek"
@app.route("/")
def index():
    if not session.get("name"):
        return render_template("index.html")

    return redirect("/store")

@app.route("/login", methods = ["POST"])
def login():
    if not request.form.get("name"):
        return redirect("/")

    session["name"] = request.form.get("name")
    return redirect("/store")

@app.route("/store")
def store():
    db = sqlite3.connect("store.db")
    c = db.cursor()
    c.execute("SELECT * FROM shopitem")
    ITEMS = c.fetchall()
    print(ITEMS)
    db.close()
    return render_template("store.html", items=ITEMS)


@app.route("/setcart", methods=["POST"])
def setcart():
    if "cart" not in session:
        print("TR")
        session["cart"] = []
    session.modified = True
    id = request.form.get("id")
    if id:
        session["cart"].append(id)
        print("POST : " + id)
        print(session["cart"])

    return redirect("/cart")
    

@app.route("/cart", methods = ["GET", "POST"])
def cart():

    if "cart" not in session:
        session["cart"] = []
            
    if request.method == "POST":
        session.modified = True
        id = request.form.get("id")
        if id:
            session["cart"].append(id)
            print("POST : " + id)
            print(session["cart"])

        return redirect("/cart")
        

    db = sqlite3.connect("store.db")
    c = db.cursor()
    tuple_str = ",".join(session["cart"])
    cmd = "SELECT * FROM shopitem WHERE id IN ({});".format(tuple_str)
    c.execute(cmd)
    CART_ITEMS = c.fetchall()
    print(session["cart"])
    print(CART_ITEMS)
    
    db.close()
    return render_template("cart.html", cart_item=CART_ITEMS)
    