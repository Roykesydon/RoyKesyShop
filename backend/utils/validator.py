import re


class Validator:
    global connection

    def __init__(self):
        self._errors = []

    def required(self, params):
        if len([x for x in params if x is None]) > 0:
            self._errors.append("Information is incomplete")

    def is_letter_number_only(self, str):
        if re.match("^[A-Za-z0-9]*$", str):
            return True
        return False

    def check_email(self, input, letterNumberOnly=False):
        if letterNumberOnly == True and self.is_letter_number_only(input) == False:
            self._errors.append("Email has illegal characters")
            return

        regex = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        if (
            input is None
            or re.search(regex, input) is None
            or len(input) < 3
            or len(input) > 50
        ):
            self._errors.append("Email format is wrong")

    def check_password(self, input, letterNumberOnly=False):
        if letterNumberOnly == True and self.is_letter_number_only(input) == False:
            self._errors.append("Password has illegal characters")
            return

        if input is None or len(input) < 6 or len(input) > 30:
            self._errors.append("Password format is wrong")

    def get_errors(self):
        return self._errors
