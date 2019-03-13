import os
from flask import render_template, url_for, request, redirect, flash, session
from shop import app, db
from shop.models import Game, User
from shop.forms import RegistrationForm, LoginForm, SortingForm, ReviewForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    game = Game.query.all()
    form = SortingForm()
    if form.validate_on_submit():
        if form.selection.data == "AZ":
            game = Game.query.order_by(Game.title.asc()).all()
        if form.selection.data == "ZA":
            game = Game.query.order_by(Game.title.desc()).all()
        if form.selection.data == "LowtoHigh":
            game = Game.query.order_by(Game.price.asc()).all()
        if form.selection.data == "HightoLow":
            game = Game.query.order_by(Game.price.desc()).all()
    
    return render_template('home.html', games=game, title='My Video Game Store', form=form)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/game/<int:game_id>", methods=["GET", "POST"])
def game(game_id):
    game = Game.query.get_or_404(game_id)
    form = ReviewForm()
    if form.validate_on_submit():
        if form.review.data != "":
            update_this = game.query.filter_by(id=game_id).first()
            review = form.review.data
            update_this.review = review
            db.session.commit()
            flash('Your review has been submitted.')

    return render_template('game.html', game=game, form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created.  You can now log in.')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('You are now logged in.')
            return redirect(url_for('home'))
        flash('Invalid password.')

        return render_template('login.html', form=form)

    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

#Flask lab 3: implementation of Cart.  Needs 'session' import!
# https://github.com/kkschick/ubermelon-shopping-app/blob/master/melons.py MELONS

@app.route("/add_to_cart/<int:game_id>")
def add_to_cart(game_id):
    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(game_id)

    flash("The game has been added to your shopping cart!")
    return redirect("/cart")

@app.route("/cart", methods=['GET', 'POST'])
def cart_display():
    if "cart" not in session:
        flash('There is nothing in your cart.')
        return render_template("cart.html", display_cart = {}, total = 0)
    else:
        items = session["cart"]
        cart = {}

        total_price = 0
        total_quantity = 0
        for item in items:
            game = Game.query.get_or_404(item)

            total_price += game.price
            if game.id in cart:
                cart[game.id]["quantity"] += 1
            else:
                cart[game.id] = {"quantity":1, "title": game.title, "price":game.price}
            total_quantity = sum(item['quantity'] for item in cart.values())


        return render_template("cart.html", title='Your Shopping Cart', display_cart = cart, total = total_price, total_quantity = total_quantity)

    return render_template('cart.html')

@app.route("/add_to_wish/<int:game_id>")
def add_to_wish(game_id):
    if "wish" not in session:
        session["wish"] = []

    session["wish"].append(game_id)

    flash("The game has been added to your wish list!")
    return redirect("/wish")

@app.route("/wish", methods=['GET', 'POST'])
def wish_display():
    if "wish" not in session:
        flash('There is nothing in your wishlist.')
        return render_template("wish.html", display_wish = {}, total = 0)
    else:
        items = session["wish"]
        wish = {}

        total_price = 0
        total_quantity = 0
        for item in items:
            game = Game.query.get_or_404(item)

            total_price += game.price
            if game.id in wish:
                wish[game.id]["quantity"] += 1
            else:
                wish[game.id] = {"quantity":1, "title": game.title, "price":game.price}
            total_quantity = sum(item['quantity'] for item in wish.values())


        return render_template("wish.html", title='Your Wish List', display_wish = wish, total = total_price, total_quantity = total_quantity)

    return render_template('wish.html')

@app.route("/delete_game/<int:game_id>", methods=['GET', 'POST'])
def delete_game(game_id):
    if "cart" not in session:
        session["cart"] = []

    session["cart"].remove(game_id)

    flash("The game has been removed from your shopping cart!")

    session.modified = True

    return redirect("/cart")

@app.route("/delete_game_wish/<int:game_id>", methods=['GET', 'POST'])
def delete_game_wish(game_id):
    if "wish" not in session:
        session["wish"] = []

    session["wish"].remove(game_id)

    flash("The game has been removed from your wish list!")

    session.modified = True

    return redirect("/wish")


@app.route("/checkout")
def checkout():
    return render_template('checkout.html', title='Checkout')





