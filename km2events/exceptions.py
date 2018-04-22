

class KM2EventsError(Exception):
    return_code = 1

    def __init__(self, message):
        self.message = message


class UUIDDuplicityError(KM2EventsError):
    return_code = 2

    def __init__(self, uuid):
        super().__init__("UUID duplicity: " + uuid)


class UnknownUUIDError(KM2EventsError):
    return_code = 3

    def __init__(self, uuid):
        super().__init__("Unknown UUID: " + uuid)
