from enum import Enum


# Stream direction for Requests
class StreamDirection(Enum):
    UNKNOWN = -1
    UPSTREAM = 1
    DOWNSTREAM = 0


# Request type enum
class RequestMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
