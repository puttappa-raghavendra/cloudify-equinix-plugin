class NotFoundExcpetion(Exception):
    def __init__(self, message):
        super().__init__(message)
        
class ServerNotAvailable(Exception):
    def __init__(self, message):
        super().__init__(message)

