from enum import StrEnum


class MyHttpException(StrEnum):

    INVALID_TOKEN = "Invalid token"
    NOT_FOUND = "Resource not found"
    UNAUTHORIZED = "You are unauthorized"
    OTHER_ERROR = "Something went wrong"
    NAME_IS_TAKEN = "Name or other resource is already taken"
    FORBIDDEN = "No access"
    BAD_REQUEST = "Error during image processing"
    INVALID_NUMBER_VALUES = "The price or quantinty cannot be lower than 0"
    INVALID_IMAGE_SIZE = "Size is empty"
    INVALID_IMAGE_FORMAT = "File is not JPG or PNG"
    INVALID_PASSWORD = "Invalid password"
