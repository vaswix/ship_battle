class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return 'Вы попали мимо доски, повторите попытку'


class BoardAlreadyHitException(BoardException):
    def __str__(self):
        return 'Вы опять попали в ту же клетку'


class BoardWrongShipException(BoardException):
    pass
