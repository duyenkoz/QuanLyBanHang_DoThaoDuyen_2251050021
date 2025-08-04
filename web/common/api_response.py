from enum import Enum

class APIResponse:
    def __init__(self, data=None, message="Success", status_code=1):
        self.data = data
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {
            "data": self.data,
            "message": self.message,
            "status_code": self.status_code
        }
    
class ResponseStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

