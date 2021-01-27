'''This module conatins the classes UserStatus and UserStatusCollection'''
# pylint: disable=R0903


class UserStatus():
    '''This class store information related to a user status update.'''

    def __init__(self, status_id, user_id, status_text):
        '''creates a UserStatus'''
        self.status_id = status_id
        self.user_id = user_id
        self.status_text = status_text


class UserStatusCollection():
    '''This class contains a database of UserStatus objects, and
    various functions to manipulate those UserStatus objects.'''

    def __init__(self):
        self.database = {}

    def add_status(self, status_id, user_id, status_text):
        '''This adds a status to the database.'''
        if status_id in self.database:
            # Rejects new status if status_id already exists
            return False
        new_status = UserStatus(status_id, user_id, status_text)
        self.database[status_id] = new_status
        return True

    def modify_status(self, status_id, user_id, status_text):
        '''This changes the stored content in a status.'''
        if status_id not in self.database:
            # Rejects update is the status_id does not exist
            return False
        self.database[status_id].user_id = user_id
        self.database[status_id].status_text = status_text
        return True

    def delete_status(self, status_id):
        '''This deletes a status.'''
        if status_id not in self.database:
            # Fails if status does not exist
            return False
        del self.database[status_id]
        return True

    def search_status(self, status_id):
        '''The returns a status.'''
        if status_id not in self.database:
            # Fails if the status does not exist
            return UserStatus(None, None, None)
        return self.database[status_id]
