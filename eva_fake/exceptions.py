import json


class RequestException(Exception):
    def __init__(self, code, message):
        self.code = code
        super(Exception, self).__init__(json.dumps({'code': code, 'message': message}))


class HttpException(Exception):
    def __init__(self, code, message):
        self.code = code
        super(Exception, self).__init__(json.dumps({'code': code, 'message': message}))


class TimeOutHttpException(HttpException):
    def __init__(self, code=None, message=None):
        if not code:
            code = 400
        if not message:
            message = 'Wait Time OUt'
        super(TimeOutHttpException, self).__init__(code, message)