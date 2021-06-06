from sacco import db, login_manager
from sacco import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    fname = db.Column(db.String(length=30), nullable=False, unique=True)
    lname = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    approved = db.Column(db.Integer(), nullable=False, default=0)
    #contributions = db.relationship('Contribution', backref='owned_user', lazy=True)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >=4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

    def can_sell(self, item_obj):
        return item_obj in self.items


class Contributions(db.Model):
    transaction_id = db.Column(db.Integer(), primary_key=True)
    transaction_date = db.Column(db.String(length=20), nullable=False)
    transaction_type = db.Column(db.String(length=20), nullable=False)
    amount = db.Column(db.Integer(), nullable=False)
    mpesa_code = db.Column(db.String(length=20), nullable=False, unique=True)
    #username = db.Column(db.Integer(), db.ForeignKey('user.username'))