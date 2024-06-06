import os

from videopy.form import AbstractField, AbstractFieldFactory
from textual.widgets import Input
from textual.validation import Validator, ValidationResult


class IsDirectoryValidator(Validator):

    def validate(self, value: str) -> ValidationResult:
        if not os.path.isdir(value):
            return self.failure("Not a directory")

        return self.success()


class Field(AbstractField):

    def __init__(self, form, field_type, name, label, required):
        super().__init__(form, field_type, name, label, required)

    def render(self) -> Input:
        return Input(
            type="text",
            name=self.name,
            validators=[IsDirectoryValidator()],
            validate_on=["submitted"],
        )


class FieldFactory(AbstractFieldFactory):
    def from_yml(self, field_yml, name, form):
        return Field(form, field_yml['type'], name, field_yml['label'], field_yml['required'])
