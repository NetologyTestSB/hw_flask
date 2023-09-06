import pydantic
import typing
from errors import HttpError


def validate(validation_schema, validation_data):
    try:
        model = validation_schema(**validation_data)
        return model.dict(exclude_none=True)
    except pydantic.ValidationError as err:
        raise HttpError(400, err.errors())


class CreateUser(pydantic.BaseModel):

    email: str
    password: str

    @pydantic.validator('password')
    def secure_password(cls, value):
        if len(value) < 8:
            raise ValueError('Password is too short')
        return value


class UpdateUser(pydantic.BaseModel):

    email: typing.Optional[str]
    password: typing.Optional[str]

    @pydantic.validator('password')
    def secure_password(cls, value):
        if len(value) < 8:
            raise ValueError('Password is too short')
        return value


class CreateAds(pydantic.BaseModel):

    header: str
    text: typing.Optional[str]
    owner_id: int


class UpdateAds(pydantic.BaseModel):

    header: str
    text: typing.Optional[str]
