from videopy.form import AbstractField, AbstractFieldFactory
from textual.widgets import Select


class Field(AbstractField):

    def __init__(self, form, field_type, name, label, configuration, required, description=""):
        super().__init__(form, field_type, name, label, required, description)

        self.configuration = configuration

        for resolution in self.configuration['resolutions']:
            if not isinstance(resolution, str):
                raise ValueError("Resolution must be a string")
            if not resolution.count("x") == 1:
                raise ValueError("Resolution must contain exactly one 'x' character")

    def render(self):
        return Select(((resolution, resolution) for resolution in self.configuration['resolutions']),
                      allow_blank=not self.required)

    def get_value(self):
        resolution = self.widget.value.split("x")

        return [int(resolution[0]), int(resolution[1])]


class FieldFactory(AbstractFieldFactory):
    def from_yml(self, field_yml, name, form):
        configuration = field_yml['configuration'] if 'configuration' in field_yml else {}

        return Field(form, field_yml['type'], name, field_yml['label'], configuration, field_yml['required'], field_yml['description'])
