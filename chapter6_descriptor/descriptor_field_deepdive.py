class Validation:

    def __init__(self, validation_function, error_msg: str):
        self.validation_function = validation_function
        self.error_msg = error_msg

    def __call__(self, value):
        if not self.validation_function(value):
            raise ValueError(f"{value!r} {self.error_msg}")


class Field:

    def __init__(self, *validations):
        """ iterable values 를 validations 로 받는다.

        :param validations:
        """
        self._name = None
        self.validations = validations

