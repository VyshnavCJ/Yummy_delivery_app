from market import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request
from market.models import User, Hotel, Customer
from market.forms import RegisterForm, LoginForm, Add_Item_Form, Update_Item_Form, Order_Item_Form, Request_Accept_Form, \
    Order_Received_Form
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():

        user_to_create = User(username=form.username.data,
                              real_name=form.real_name.data,
                              email_address=form.email_address.data,
                              phone_num=form.phone_num.data,
                              role=form.role.data,
                              address=form.address.data)
        password_hash = bcrypt.generate_password_hash(form.password1.data).decode('utf-8')
        user_to_create.password_hash = password_hash
        user_to_create.save()
        login_user(user_to_create)
        flash(f'Account has been created in the name of {user_to_create.username}', category='success')
        if current_user.role == 1:
            return redirect(url_for('hotel_page'))
        else:
            return redirect(url_for('customer_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category="danger")
    return render_template('register.html', form=form)


@app.route('/customer')
@login_required
def customer_page():
    return render_template('customer.html')


@app.route('/hotel', methods=['GET', 'POST'])
@login_required
def hotel_page():
    update_form = Update_Item_Form()
    if request.method == 'POST':
        update_item = request.form.get('update_item')
        return redirect(url_for('update_page', item=update_item))
    return render_template('hotel.html', Hotel=Hotel, form=update_form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.objects(username=form.username.data).first()
        if attempted_user and bcrypt.check_password_hash(attempted_user.password_hash, form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            if attempted_user.role == 1:
                return redirect(url_for('hotel_page'))
            else:
                return redirect(url_for('customer_page'))
        else:
            flash(f'User name and password are not match! please try again', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash(f'You have been logged out!', category='info')
    return redirect(url_for("home_page"))


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    form = Add_Item_Form()
    if form.validate_on_submit():
        item_to_add = Hotel(name=form.name.data,
                            price=form.price.data,
                            quantity=form.quantity.data)
        item_to_add.add(current_user)
        item_to_add.save()
        flash(f'Successfully added {item_to_add.name}', category='success')
        return redirect(url_for('hotel_page'))
    return render_template('add.html', form=form)


@app.route('/update_item/<item>', methods=['GET', 'POST'])
def update_page(item):
    form = Update_Item_Form()
    if form.validate_on_submit():
        updating_item = Hotel.objects.get(name=item)
        updating_item.update(price=form.price.data, quantity=form.quantity.data)
        updating_item.save()
        flash(f'Successfully updated {updating_item.name}', category='success')
        return redirect(url_for('hotel_page'))
    return render_template('update.html', form=form, item=item)


@app.route('/order_items', methods=['GET', 'POST'])
def order_page():
    form = Order_Item_Form()
    if request.method == 'POST' and form.validate_on_submit():
        order_item_name = request.form.get('order_item_name')
        order_item_hotel_username = request.form.get('user_username')
        order_item_price = request.form.get('order_item_price')
        hotel_item = Hotel.objects.get(name=order_item_name)
        if hotel_item.can_purchase(form.quantity_needed.data):
            ordered_item = Customer(name=order_item_name,
                                    price=order_item_price,
                                    quantity=form.quantity_needed.data,
                                    hotel_user=order_item_hotel_username)
            quantity = form.quantity_needed.data
            hotel_item.quantity_decrease(quantity)
            ordered_item.user_buy(current_user)
            ordered_item.save()
            hotel_item.save()
            flash(f'Successfully Ordered {ordered_item.name} for {ordered_item.price}$', category='success')
            return redirect(url_for('customer_page'))
        else:
            flash(f"Unfortunately, We don't have that much of {order_item_name} right now!", category='danger')
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with ordering item: {err_msg}', category="danger")
    return render_template('order.html', Hotel=Hotel, User=User, form=form)


@app.route('/order_status', methods=['GET', 'POST'])
def order_status():
    form = Order_Received_Form()
    if form.validate_on_submit() and request.method == 'POST':
        received_id = request.form.get('received_item_id')
        item = Customer.objects.get(id=received_id)
        item.received()
        item.save()
        return redirect(url_for('customer_page'))
    return render_template('status.html',
                           Customer=Customer,
                           hotel=User,
                           form=form)


@app.route('/history')
def history_page():
    customer_order = Customer.objects(owner=current_user.username)
    return render_template('history.html',
                           orders=customer_order,
                           hotel=User)


@app.route('/requests', methods=['GET', 'POST'])
def order_requests():
    form = Request_Accept_Form()
    if form.validate_on_submit() and request.method == 'POST':
        request_id = request.form.get('request_item_id')
        item = Customer.objects.get(id=request_id)
        item.accepted()
        item.save()
        return redirect(url_for('hotel_page'))
    return render_template('request.html', Customer=Customer, customer=User, form=form)
