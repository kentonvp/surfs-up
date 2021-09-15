
class UserInfoNotFoundException(Exception):
    '''
    User's information is not found.
    '''
    pass

class InvalidSchemaException(Exception):
    '''
    Database schema does not match.
    '''
    pass