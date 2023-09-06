import psycopg2
from errors import HttpError
from models import Session, Advertising
from flask import jsonify, request
from flask.views import MethodView
from schema import validate
import schema
from sqlalchemy.exc import IntegrityError


def get_ads(session, ads_id):
    ads = session.get(Advertising, ads_id)
    if ads is None:
        raise HttpError(404, "ads not found")
    return ads


class AdsView(MethodView):

    def get(self, ads_id: int):
        with Session() as session:
            ads = get_ads(session, ads_id)
            return jsonify(
                {
                    "id": ads.id,
                    "header": ads.header,
                    "creation_time": ads.creation_time.isoformat(),
                    "text": ads.text,
                    "owner": ads.owner_id
                }
            )

    def post(self):
        validated_json = validate(schema.CreateAds, request.json)
        with Session() as session:
            ads = Advertising(**validated_json)
            session.add(ads)
            try:
                session.commit()
            except IntegrityError as er:
                if isinstance(er.orig, psycopg2.errors.UniqueViolation):
                    raise HttpError(409, "advertising already exists")
            return jsonify({"id": ads.id})


    def patch(self, ads_id: int):
        validated_json = validate(schema.UpdateAds, request.json)
        with Session() as session:
            ads = get_ads(session, ads_id)
            for field, value in validated_json.items():
                setattr(ads, field, value)
            session.add(ads)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, "advertising already exists")
            return jsonify({"id": ads.id, "header": ads.header})


    def delete(self, ads_id: int):
        with Session() as session:
            ads = get_ads(session, ads_id)
            session.delete(ads)
            session.commit()
            return jsonify({"status": "success"})
