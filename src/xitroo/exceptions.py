class InvalidLocale(Exception):pass
class CaptchaException(Exception):pass
class EmailNotFound(Exception):pass

class GETRequestException(Exception):
    def __init__(self, classname: str, text: str, code: int):
        super().__init__("Could not get " + classname + ": "+text+" with code: "+code.__str__())

class POSTRequestException(Exception):
    def __init__(self, classname: str, text: str, code: int):
        super().__init__("Could not send " + classname + ": "+text+" with code: "+code.__str__())
