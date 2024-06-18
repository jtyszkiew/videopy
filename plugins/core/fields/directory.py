import os

from videopy.form import AbstractField, AbstractFieldFactory
from textual.widgets import Input
from textual.validation import Validator, ValidationResult


class IsDirectoryValidator(Validator):

    def __init__(self, required):
        super().__init__()

        self.required = required

    def validate(self, value: dict) -> ValidationResult:
        if not value['directory'] and not self.required:
            return self.success()
        if not value['directory'] and self.required:
            return self.failure("Required")
        if not os.path.isdir(value['directory']):
            return self.failure("Not a directory")

        return self.success()


class Field(AbstractField):

    def __init__(self, form, field_type, name, label, required, description=""):
        super().__init__(form, field_type, name, label, required, description)

    def render(self) -> Input:
        return Input(
            type="text",
            name=self.name,
            validators=[IsDirectoryValidator(self.required)],
            validate_on=["submitted"],
        )

    def get_value(self):
        return {
            "directory": self.widget.value
        }


class FieldFactory(AbstractFieldFactory):
    def from_yml(self, field_yml, name, form):
        return Field(form, field_yml['type'], name, field_yml['label'], field_yml['required'], field_yml['description'])
