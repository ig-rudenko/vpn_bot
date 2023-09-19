class ProfileException(Exception):
    def __init__(self, message: str):
        self.message = message


class ProfileAlreadyExist(ProfileException):
    pass


class ProfileDataInvalid(ProfileException):
    pass