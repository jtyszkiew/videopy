from videopy.form import AbstractField, AbstractFieldFactory
from textual.widgets import Input


class Field(AbstractField):

    def __init__(self, form, field_type, name, label, configuration, required, description=""):
        super().__init__(form, field_type, name, label, required, description)

        self.configuration = configuration

    def render(self):
        return Input(
            type="text",
            name=self.name,
        )

    def get_value(self):
        return {
            "text": self.widget.value
        }


class FieldFactory(AbstractFieldFactory):
    def from_yml(self, field_yml, name, form):
        configuration = field_yml['configuration'] if 'configuration' in field_yml else {}

        return Field(form, field_yml['type'], name, field_yml['label'], configuration, field_yml['required'],
                     field_yml['description'])
