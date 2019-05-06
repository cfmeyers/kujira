from unittest.mock import MagicMock


from pytest import fixture
from kujira.models.user import UserModel


@fixture
def vader_user():
    return UserModel(
        email='dvader@empire.com',
        name='dvader',
        key='dvader',
        display_name='Darth Vader',
    )


class TestUserModel:
    def test_it_has_user_fields(self, vader_user):
        assert 'dvader@empire.com' == vader_user.email
        assert 'dvader' == vader_user.key
        assert 'dvader' == vader_user.name
        assert 'Darth Vader' == vader_user.display_name

    def test_it_can_serialize_itself_from_api(self):
        api_user = MagicMock(
            emailAddress='dvader@empire.com',
            displayName='Darth Vader',
            key='dvader',
            name='dvader',
        )
        user = UserModel.from_API(api_user)
        assert 'dvader@empire.com' == user.email
        assert 'dvader' == user.key
        assert 'Darth Vader' == user.display_name

    def test_it_serializes_itself_to_string(self, vader_user):
        as_string = str(vader_user)
        assert '[dvader] [dvader] [Darth Vader] [dvader@empire.com]' == as_string

    def test_two_users_with_the_same_attributes_are_the_same(self, vader_user):
        vader_user_2 = UserModel(
            email='dvader@empire.com',
            name='dvader',
            key='dvader',
            display_name='Darth Vader',
        )

        assert vader_user == vader_user_2

    def test_it_deserializes_itself_from_string(self, vader_user):
        string_vader = '[dvader] [dvader] [Darth Vader] [dvader@empire.com]'
        assert vader_user == UserModel.from_string(string_vader)
