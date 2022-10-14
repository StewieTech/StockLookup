import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Global Variables




# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")




@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # return "Hello world"
    return apology("Click Buy in the top menu")
    # return apology("Show portfolio of Stocks here")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    user_id = session["user_id"]
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    counter = cash[0]
    counter = counter['cash']
    today = date.today()
    if request.method == "POST":
        quotes = lookup(request.form.get("quote"))
        shares = int(request.form.get("shares"))

        print(shares)
        print(user_id)
        if quotes == None:
            return apology("Stock Ticker Does Not Exist!!!!", 403)
        if not shares > 0:
            return apology("Postive Shares Only!", 403)


        Qname = (quotes['name'])
        Qprice = (quotes['price'])
        Qsymbol = (quotes['symbol'])
        purchase = int(Qprice) * int(shares)
        counter -= purchase




        print(quotes)
        print(Qsymbol)
        print(purchase)
        print(counter)
        print(today)

        db.execute("Update users SET cash = ? WHERE id = ?", counter, user_id )
        db.execute("INSERT INTO Stocks (SNAME, SPRICE, SAMOUNT, STOTAL, SCASH, purchase_date, user_ID) VALUES(?, ?, ?, ?, ?, ?, ?)", Qname, Qprice, shares, purchase, counter, today, user_id)

        # elif quotes != None:
        return render_template("buy.html", QnameR=Qname,QpriceR=Qprice, QsymbolR=Qsymbol, cashR=counter )
        # return lookup(quote)

    else:

        Portfolio = db.execute("SELECT * FROM users where id = ?", user_id)
        return render_template("buy.html", Portfolio=Portfolio, cashR=counter)
        # return render_template("buy.html")
        # TODO: Display the entries in the database on index.html




    return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        quotes = lookup(request.form.get("quote"))
        if quotes == None:
            return apology("Stock Ticker Does Not Exist!", 403)

        Qname = (quotes['name'])
        Qprice = (quotes['price'])
        Qsymbol = (quotes['symbol'])

        print(quotes)
        print(quotes['name'])
        print(Qsymbol)

        # elif quotes != None:
        return render_template("quote.html", QnameR=Qname,QpriceR=Qprice, QsymbolR=Qsymbol )
        # return lookup(quote)

    else:
        return render_template("quote.html")
    return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        # Ensure username was submitted
        cpassword = request.form.get("cpassword")
        secure = generate_password_hash(password)
        check = db.execute("SELECT COUNT(*) FROM users WHERE username = :username", username=username)
        print(username)
        print(check)
        test = [{'COUNT(*)': 0}]
        print(test)
        print(secure)
        # usernamecheck = db.execute("SELECT COUNT(*) FROM users WHERE username = :username", username)
        if password != cpassword:
            return apology("Passwords must match!", 403)

          # Query database for username
        elif test != check:
            return apology("Username already exists!!", 403)

    # Ensure password was submitted
        elif password == cpassword:

            # TODO: Add the user's entry into the database
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, secure)
            return redirect("/")

    #  return redirect("/")
    #   name = request.form.get("name", "world")
    #   return render_template("index.html", name=name)

    else:
        #  username = request.form.get("username")
        #  password = request.form.get("password")
        #  db.execute("INSERT INTO finance (username, hash) VALUES(?, ?)", username, password)
        #  return redirect("/register")
        return render_template("register.html")
        # registrants = db.execute("SELECT * FROM birthdays")
        # return render_template("index.html", registrants=registrants)
        # # TODO: Display the entries in the database on index.html

        # return redirect("/")

    # return apology("TODO")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")

if __name__ == '__main__':
    app.debug = True
    app.run()
    

    # **  To Do **
# Require that a user input a username, implemented as a text field whose name is username.
# Require that a user input a password, implemented as a text field whose name is password,
# Submit the user’s input via POST to /register.

# ** check **
#  Render an apology if the user’s input is blank or the username already exists.
#  and then that same password again, implemented as a text field whose name is confirmation.
# Render an apology if either input is blank or the passwords do not match.

# INSERT the new user into users, storing a hash of the user’s password, not the password itself. Hash the user’s password with generate_password_hash Odds are you’ll want to create a new template (e.g., register.html) that’s quite similar to login.html.
# Once the user is registered, you may either automatically log in the user or bring the user to a page where they can log in themselves.

# API key = pk_82caa2b999f54c56ad83bf7e46409fd2
# export API_KEY=pk_82caa2b999f54c56ad83bf7e46409fd2
# set API_KEY=pk_82caa2b999f54c56ad83bf7e46409fd2
# py -m venv env
# env\Scripts\activate
# FLASK_ENV = development
