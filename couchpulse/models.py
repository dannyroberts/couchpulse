from jsonobject import *


class RequestLog(JsonObject):
    type = 'request'
    id = StringProperty()
    method = StringProperty()
    path = StringProperty()
    params = DictProperty()
    size = IntegerProperty()
    time = FloatProperty()
    timestamp = FloatProperty()
    traceback = StringProperty()


class ResponseLog(JsonObject):
    type = 'response'
    id = StringProperty()
    path = StringProperty()
    method = StringProperty()
    size = IntegerProperty()
    time = FloatProperty()
