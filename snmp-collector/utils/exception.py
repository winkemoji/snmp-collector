class KeyUniqueException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
        self._message = message

    def __str__(self):
        return self._message
