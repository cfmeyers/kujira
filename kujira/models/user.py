import re


class UserModel:
    def __init__(self, name, key, email, display_name):
        self.name = name
        self.key = key
        self.email = email
        self.display_name = display_name

    @classmethod
    def from_API(cls, api_user):
        return cls(
            email=api_user.emailAddress,
            name=api_user.name,
            key=api_user.key,
            display_name=api_user.displayName,
        )

    @classmethod
    def from_string(cls, str_user):
        key, name, display_name, email = re.findall(r"\[(.+?)\]", str_user)
        return cls(email=email, name=name, key=key, display_name=display_name)

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.email == other.email
            and self.display_name == other.display_name
            and self.key == other.key
        )

    def __str__(self):
        return f'[{self.key}] [{self.name}] [{self.display_name}] [{self.email}]'
