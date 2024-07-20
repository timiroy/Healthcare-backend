class ServiceException(Exception):
    def __init__(self, message, *args: object) -> None:
        super().__init__(*args)

        self.message = message


class NotFoundException(ServiceException): ...


class RecordExistsException(ServiceException):
    def __init__(self, message, record=None, *args: object) -> None:
        super().__init__(message, *args)

        self.record = record


class BadRequestException(ServiceException): ...