from videopy.form import AbstractField, AbstractFieldFactory
from textual.app import ComposeResult
from textual.widgets import Static, Input
from textual.widget import Widget
from textual.containers import Horizontal


class OutputPath(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.directory = Input(placeholder="Directory")
        self.file_name = Input(placeholder="File Name")
        self.horizontal = Horizontal()

    def compose(self) -> ComposeResult:
        self.directory.styles.width = "70%"
        self.file_name.styles.width = "30%"

        with self.horizontal:
            yield self.directory
            yield self.file_name


class Field(AbstractField):

    def __init__(self, form, field_type, name, label, configuration, required, description=""):
        super().__init__(form, field_type, name, label, required, description)

        self.configuration = configuration

    def render(self):
        return OutputPath()

    def get_value(self):
        return f"{self.widget.directory.value}/{self.widget.file_name.value}"

    def after_render(self):
        self.widget.styles.height = 3


class FieldFactory(AbstractFieldFactory):
    def from_yml(self, field_yml, name, form):
        configuration = field_yml['configuration'] if 'configuration' in field_yml else {}

        return Field(form, field_yml['type'], name, field_yml['label'], configuration, field_yml['required'],
                     field_yml['description'])
