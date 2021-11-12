from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.objects(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exits! Please try different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.objects(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email already exits! Please try different EmailID')

    def validate_phone_num(self, phone_num_to_check):
        phone_num = User.objects(phone_num=phone_num_to_check.data).first()
        if phone_num:
            raise ValidationError('Phone Number already exits! Please try different EmailID')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    real_name = StringField(label='Real Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    phone_num = IntegerField(label='Phone Number:', validators=[DataRequired()])
    address = TextAreaField(label='Address:', validators=[DataRequired()])
    role = SelectField(label='Role:', choices=[('1', 'Hotel'), ('2', 'Customer')])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Login')


class PurchaseItemForm(FlaskForm):
    Submit = SubmitField(label="Purchase Item!")


class Add_Item_Form(FlaskForm):
    name = StringField(label='Item', validators=[DataRequired()])
    price = IntegerField(label='Price', validators=[DataRequired()])
    quantity = IntegerField(label='Quantity', validators=[DataRequired()])
    submit = SubmitField(label="Add Item!")


class Update_Item_Form(FlaskForm):
    price = IntegerField(label='Price', validators=[DataRequired()])
    quantity = IntegerField(label='Quantity', validators=[DataRequired()])
    submit = SubmitField(label="Update Item!")


class Order_Item_Form(FlaskForm):
    quantity_needed = IntegerField(label='Required Quantity', validators=[DataRequired()])
    submit = SubmitField(label='Order Item!')


class Request_Accept_Form(FlaskForm):
    submit = SubmitField(label='Accept Request')


class Order_Received_Form(FlaskForm):
    submit = SubmitField(label='Order Received')

