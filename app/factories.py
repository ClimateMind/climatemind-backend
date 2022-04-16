import factory
from faker import Factory as FakerFactory
from werkzeug.security import generate_password_hash

from app.models import Users, Sessions

faker = FakerFactory.create()


class UsersFactory(factory.alchemy.SQLAlchemyModelFactory):
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    user_uuid = factory.LazyAttribute(lambda x: faker.uuid4().upper())
    user_email = factory.LazyAttribute(lambda x: faker.email())
    password = factory.LazyAttribute(lambda x: faker.password())
    password_hash = factory.LazyAttribute(lambda o: generate_password_hash(o.password))

    class Meta:
        model = Users
        exclude = ("password",)


class SessionsFactory(factory.alchemy.SQLAlchemyModelFactory):
    ip_address = factory.LazyAttribute(lambda x: faker.ipv4())
    user = factory.SubFactory(UsersFactory)
    session_uuid = factory.LazyAttribute(lambda x: faker.uuid4().upper())
    session_created_timestamp = factory.LazyAttribute(lambda x: faker.date_time())

    class Meta:
        model = Sessions
