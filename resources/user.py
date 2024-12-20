from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
import requests
import os

from db import db
from models import UserModel
from schemas import UserSchema, UserRegisterSchema
from blocklist import BLOCKLIST


blp = Blueprint("Users", "users", description="Operations on users")


def send_simple_message(to, subject, body):

    mailgun_domain = os.getenv('MAILGUN_DOMAIN')
    mailgun_api_key = os.getenv('MAILGUN_API_KEY')
    return requests.post(f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
                         auth=("api", mailgun_api_key),
                         data={"from": f"Daniel Gardez <mailgun@{mailgun_domain}>",
                         "to": [to],
                         "subject": subject,
                         "text": body})


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        # Use flush=True for printing
        #print("Jorl", UserModel.query.filter(UserModel.username == user_data["username"]).first().id, flush=True)
        
        if UserModel.query.filter(
            or_(
                UserModel.username == user_data["username"],
                UserModel.email == user_data["email"]
            )
        ).first():
            abort(409, message="A user with that username already exists.")
            
        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()

        send_simple_message(to=user.email,
                           subject="Successfully signed up!",
                           body=f"Hi, {user.username}, keep up the good work!")

        return {"message": "User created successfully."}, 201
    

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        print(pbkdf2_sha256.verify(user_data["password"], user.password))

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        
        abort(401, message="Invalid credentials.")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}
    

@blp.route("/user/<int:user_id>")
class User(MethodView):
    """
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful
    when we are manipulating data regarding the users.
    """

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200
