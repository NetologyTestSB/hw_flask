from hashlib import md5
from errors import HttpError
from models import Session, User
from flask import jsonify, request
from flask.views import MethodView
from schema import validate
import schema
from sqlalchemy.exc import IntegrityError


def hash_password(password: str):
    password = password.encode()
    password = md5(password).hexdigest()
    return password


def get_user(session, user_id):
    user = session.get(User, user_id)
    if user is None:
        raise HttpError(404, "user not found")
    return user


class UserView(MethodView):
    def get(self, user_id):
        with Session() as session:
            user = get_user(session, user_id)
            return jsonify(
                {
                    "id": user.id,
                    "email": user.email,
                    "creation_time": user.creation_time.isoformat(),
                }
            )

    def post(self):
        validated_json = validate(schema.CreateUser, request.json)
        validated_json["password"] = hash_password(validated_json["password"])
        with Session() as session:
            user = User(**validated_json)
            session.add(user)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, "User already exists")
            return jsonify({"id": user.id})

    def patch(self, user_id):
        validated_json = validate(schema.UpdateUser, request.json)
        if "password" in validated_json:
            validated_json["password"] = hash_password(validated_json["password"])
        with Session() as session:
            user = get_user(session, user_id)
            for field, value in validated_json.items():
                setattr(user, field, value)
            session.add(user)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, "User already exists")
            return jsonify({"id": user.id})

    def delete(self, user_id):
        with Session() as session:
            user = get_user(session, user_id)
            session.delete(user)
            session.commit()
            return jsonify({"status": "success"})
