from flask import Flask, render_template, flash, request, redirect, url_for, session
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from passlib.hash import sha256_crypt
from bson.objectid import ObjectId
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

# ✅ FIXED MONGO URI
uri = "mongodb+srv://Techg:4KTgpt999@cluster0.a3m57k5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["orderdb"]
orders = db["orders"]

admin_db = client["master"]
master = admin_db["self-master"]

bundles = {
    "mtn": [
        "1GB — ₵4.99", "2GB — ₵9.50", "3GB — ₵13.99", "4GB — ₵18.99",
        "5GB — ₵23.99", "6GB — ₵28.50", "8GB — ₵37.50",
        "10GB — ₵44.99", "15GB — ₵66.00", "20GB — ₵86.50"
    ]
}

# ================= HOME =================
@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        bundle = request.form.get("bundle-select")
        recipient = request.form.get("username")

        orders.insert_one({
            "bundle": bundle,
            "recipient": recipient,
            "status": "Pending"
        })

        flash("Order submitted successfully. Proceed to payment.")
        return redirect(url_for("homepage"))

    return render_template("main.html", bundles=bundles)

# ================= ADMIN LOGIN =================
@app.route("/self-master", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = master.find_one({"email": email})
        if user and sha256_crypt.verify(password, user["password"]):
            session["admin"] = email
            return redirect(url_for("dashboard"))

        flash("Wrong email or password")

    return render_template("login.html")

# ================= DASHBOARD =================
@app.route("/dh-msttq")
def dashboard():
    if "admin" not in session:
        return redirect(url_for("admin"))

    return render_template("dashboard.html", orders=orders.find())

# ================= MARK DELIVERED =================
@app.route("/deliver/<order_id>", methods=["POST"])
def deliver(order_id):
    if "admin" not in session:
        return redirect(url_for("admin"))

    orders.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": "Delivered"}}
    )
    return redirect(url_for("dashboard"))

# ================= DELETE =================
@app.route("/delete/<order_id>", methods=["POST"])
def delete_card(order_id):
    if "admin" not in session:
        return redirect(url_for("admin"))

    orders.delete_one({"_id": ObjectId(order_id)})
    return redirect(url_for("dashboard"))

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run(debug=True)
