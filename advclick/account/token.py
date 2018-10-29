import base64
import time

# My first Python class

# About one month
EXPIRED_TIME = 60 * 60 * 24 * 1 * 1000
DIVIDER = ":"
ASCII = 'ascii'


class Token:
    """
    This class is used for Token encode and decode.
    """

    def __init__(self, user_id=None, user_name=None, token=None):
        """
            Constructor with user_id & user_name ,this is an encoding process
        """
        if user_id is not None:
            print("Token1 user_id -> " + str(user_id) + " user_name -> " + user_name)
            self.raw_str = str(user_id) + DIVIDER + user_name + DIVIDER + str(time.time())
            self.encode_str = Token.encode_token(self.raw_str)
        else:
            print("Token2 token -> " + str(token))
            self.raw_str = Token.decode_token(token)
            self.encode_str = token

        print("raw_str -> " + self.raw_str)
        print("encode_str -> " + str(self.encode_str))
        self.raw_array = self.raw_str.split(DIVIDER)
        print("raw_array -> " + str(self.raw_array))

    @staticmethod
    def encode_token(values):
        token = base64.b64encode(values.encode(ASCII))
        return token.decode(ASCII)

    @staticmethod
    def decode_token(token):
        value = base64.b64decode(token)
        return value.decode(ASCII)

    def get_time(self):
        return float(self.raw_array[2])

    def get_user_name(self):
        """ Get user name from token"""
        return self.raw_array[1]

    def get_user_id(self):
        """ Get user id from token """
        return int(self.raw_array[0])

    def verify_token(self):
        """ Verify the token expired or not"""
        current_time = time.time()
        if current_time - self.get_time() > EXPIRED_TIME:
            return False
        else:
            return True

    def get_token(self):
        return self.encode_str
