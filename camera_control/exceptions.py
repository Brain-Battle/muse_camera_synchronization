from enum import Enum

class CameraJSONErrorCodes(Enum):
    """
        An enum class representing all error codes of the
        Sony Remote Control API.
    """
    
    ERROR_ANY = 1
    ERROR_TIMEOUT = 2
    ERROR_ILLEGAL_ARGUMENT = 3
    ERROR_ILLEGAL_DATA_FORMAT = 4
    ERROR_ILLEGAL_REQUEST = 5
    ERROR_ILLEGAL_RESPONSE = 6
    ERROR_ILLEGAL_STATE = 7
    ERROR_ILLEGAL_TYPE = 8
    ERROR_INDEX_OUT_OF_BOUNDS= 9
    ERROR_NO_SUCH_ELEMENT = 10
    ERROR_NO_SUCH_METHOD = 11
    ERROR_NO_SUCH_FIELD = 12
    ERROR_NULL_POINTER = 13
    ERROR_UNSUPPORTED_VER = 14
    ERROR_UNSUPPORTED_OP = 15
    ERROR_SHOOT_FAIL = 40400
    ERROR_CAMERA_NOT_READY = 40401
    ERROR_POLLING_ALREADY_RUNNING = 40402
    ERROR_CAPTURING_NOT_FINISHED = 40403
    ERROR_CONTENT_CANNOT_DELETE = 41003

class CameraException(Exception):
    """
        Camera exception class.

        Finds the error in the CameraJSONErrorCodes class,
        and raises an according error message.
    """
    def __init__(self, error_code, message=None):
        self.error_code = CameraJSONErrorCodes(error_code)
        if message == None:
            super().__init__(str(self.error_code))

class CameraNotFoundException(Exception):
    """
        Raised when pairing process cannot find the camera.

        It might happen when the camera has already been paired.
    """
    def __init__(self):
        super().__init__("Could not find camera via UPNP")
