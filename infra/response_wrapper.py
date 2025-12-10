class ResponseWrapper:
    def __init__(self, ok, status_code, data):
        self.ok = ok
        self.status_code = status_code
        self.data = data