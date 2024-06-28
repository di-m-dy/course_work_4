"""
ru: Модуль для описания пользовательских ошибок пр работе с API.
en: Module for describing user errors when working with the API.
"""


class ApiError(Exception):
    """
    ru: Базовый класс для пользовательских ошибок.
    en: Base class for user errors.
    """
    pass


class AttrIntersectionError(ApiError):
    """
    ru: Класс ошибки для пересечения аттрибутов.
    en: Error class for attribute intersection.
    """
    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else "Attributes intersect"

    def __str__(self):
        return self.message


class AttrValueRestrictionError(ApiError):
    """
    ru: Класс ошибки для аттрибута у которого еть ограничение значения.
    en: Error class for an attribute that has a value restriction.
    """
    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else "Restriction value"

    def __str__(self):
        return self.message


class ObjectNotFoundError(ApiError):
    """
    ru: Класс ошибки для объекта, который не найден.
    en: Error class for an object that is not found.
    """

    def __init__(self, *args, **kwargs):
        self.message = f"{args[0]}" if args else "Object not found"

    def __str__(self):
        return self.message


class BadArgumentError(ApiError):
    """
    ru: Класс ошибки для неверного аргумента.
    en: Error class for an invalid argument.
    """
    def __init__(self, *args, **kwargs):
        self.message = f"{args[0]}" if args else "Bad argument"

    def __str__(self):
        return self.message


class AdditionalActionError(ApiError):
    """
    ru: Класс ошибки для дополнительного действия.
    en: Error class for additional action.
    """
    def __init__(self, *args, **kwargs):
        self.message = f"{args[0]}" if args else "Additional action"

    def __str__(self):
        return self.message


class UnknownError(ApiError):
    """
    ru: Класс ошибки для неизвестной ошибки.
    en: Error class for an unknown error.
    """
    def __repr__(self):
        return "Unknown error / Неизвестная ошибка"
