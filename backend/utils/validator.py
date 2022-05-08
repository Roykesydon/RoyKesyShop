import re


class Validator:
    global connection

    def __init__(self):
        self._errors = []

    """
    regular
    """

    def required(self, params):
        if len([x for x in params if x is None]) > 0:
            self._errors.append("Information is incomplete")

    def is_letter_number_only(self, str):
        if re.match("^[A-Za-z0-9]*$", str):
            return True
        return False

    """
    User
    """

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

    """
    Clothing
    """

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

    def check_clothing_parent_class(self, input):
        if input is None or len(input) < 1 or len(input) > 25:
            self._errors.append("Parent clothing class format is wrong")

    def check_clothing_sub_class(self, input):
        if input is None or len(input) < 1 or len(input) > 25:
            self._errors.append("Sub clothing class format is wrong")

    """
    Order
    """

    def check_address(self, input):
        if input is None or len(input) < 1 or len(input) > 100:
            self._errors.append("Address format is wrong")

    def check_phone(self, input):
        if input is None or len(input) < 1 or len(input) > 20:
            self._errors.append("Phone format is wrong")

    def check_name(self, input):
        if input is None or len(input) < 1 or len(input) > 40:
            self._errors.append("Name format is wrong")

    def check_clothing(self, input):
        if input is None or len(input) == 0:
            self._errors.append("Clothing format is wrong")
            return

        for item in input.split(","):
            if len(item.split("-")) != 3:
                self._errors.append("Clothing format is wrong")
                return

    def get_errors(self):
        return self._errors
