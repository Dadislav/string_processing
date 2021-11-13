class TooShortNicknameException(Exception):
    pass


class TooLongNicknameException(Exception):
    pass


class TooShortCommentException(Exception):
    pass


class TooLongCommentException(Exception):
    pass


class NotStringInInput(Exception):
    pass


class PossibleSqlInjection(Exception):
    pass
