import os

from videopy.form import AbstractField, AbstractFieldFactory
from textual.widgets import Input
from textual.validation import Validator, ValidationResult

from videopy.utils.file import get_file_extension


class IsMediaFileValidator(Validator):

    def __init__(self, extensions, required=True):
        super().__init__()

        self.extensions = extensions
        self.required = required

    def validate(self, value: str) -> ValidationResult:
        if (value == "" or value is None) and self.required is False:
            return self.success()

        ext = get_file_extension(value)

        if not os.path.isfile(value):
            return self.failure("Not a file")
        if ext not in self.extensions:
            return self.failure("Not a media file")

        return self.success()


class Field(AbstractField):

    def __init__(self, form, field_type, name, label, required, configuration, description=""):
        super().__init__(form, field_type, name, label, required, description)

        self.configuration = configuration

    def render(self) -> Input:
        return Input(
            type="text",
            name=self.name,
            validators=[IsMediaFileValidator(self.configuration['extensions'], self.required)],
            validate_on=["submitted"],
        )


class FieldFactory(AbstractFieldFactory):
    def from_yml(self, field_yml, name, form):
        return Field(form, field_yml['type'], name, field_yml['label'], field_yml['required'],
                     field_yml['configuration'], field_yml['description'])
