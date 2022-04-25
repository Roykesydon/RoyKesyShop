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

    def check_clothing_title(self, input):
        if input is None or len(input) < 2 or len(input) > 50:
            self._errors.append("Clothing title format is wrong")

    def check_clothing_description(self, input):
        if input is None or len(input) > 500:
            self._errors.append("Clothing description format is wrong")

    def check_clothing_cost(self, input):
        if input is None or not input.replace(".", "", 1).isdigit():
            self._errors.append("Clothing cost format is wrong")
        try:
            if float(input) > 1000000:
                self._errors.append("Clothing cost format is wrong")
        except:
            self._errors.append("Clothing cost format is wrong")

    def check_upload_picture(self, input, extension):
        """
        TODO
        """
        acceptExtensions = ["jpg", "jpeg", "png"]
        if extension not in acceptExtensions:
            self._errors.append("Image extension is not accepted")

    def check_selected_size(self, input):
        try:
            if len(input) == 0 or input == None:
                self._errors.append("Selected size format is wrong")
        except:
            self._errors.append("Selected size format is wrong")

    def get_errors(self):
        return self._errors