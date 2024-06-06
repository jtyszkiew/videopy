from videopy.form import AbstractField, AbstractFieldFactory
from textual.widgets import Select


class Field(AbstractField):

    def __init__(self, form, field_type, name, label, configuration, required):
        super().__init__(form, field_type, name, label, required)

        self.configuration = configuration

    def render(self):
        return Select(((f, f) for f in self.configuration['fps']), allow_blank=not self.required)


class FieldFactory(AbstractFieldFactory):
    def from_yml(self, field_yml, name, form):
        configuration = field_yml['configuration'] if 'configuration' in field_yml else {}

        return Field(form, field_yml['type'], name, field_yml['label'], configuration, field_yml['required'])
