class HttpError(Exception):
    """
    An Exception which can be raised inside a view. 
    It will be handle in `core.BaseView` and shown to user.
    """
    def __init__(self, code: int, text: str, *args):
        self.code = code
        self.txt = text

    def __str__(self):
        return f'[{self.code}] {self.txt}'