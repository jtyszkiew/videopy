from abc import abstractmethod
from types import NoneType

from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Header
from textual.widget import Widget
from textual.validation import ValidationResult


class AbstractField:

    def __init__(self, form, field_type, name, label, required, description=""):
        self.widget = None
        self.error_widget = None

        self.form = form
        self.type = field_type
        self.name = name
        self.label = label
        self.required = required
        self.description = description

    def do_render(self) -> Widget:
        self.widget = self.render()

        return self.widget

    def get_value(self):
        return self.widget.value

    @abstractmethod
    def after_render(self):
        pass

    @abstractmethod
    def render(self) -> Widget:
        pass

    def validate(self):
        if not hasattr(self.widget, 'validate'):
            return ValidationResult.success()

        validation = self.widget.validate(self.get_value())

        if isinstance(validation, NoneType):
            return ValidationResult.success()

        return validation


class AbstractFieldFactory:

    @abstractmethod
    def from_yml(self, field_yml, name, form):
        pass


class Form(App):
    def __init__(self):
        super().__init__()

        self.fields = []
        self.labels = []
        self.submit = None
        self.exit = None
        self.header = None

    def add_field(self, field):
        if not isinstance(field, AbstractField):
            raise ValueError("Field must be an instance of AbstractField")

        self.fields.append(field)

    def render(self):
        self.run()

    def compose(self) -> ComposeResult:
        self.header = Header(name="videopy script form")

        yield self.header

        for field in self.fields:
            label = Static(field.label)
            error = Static(classes="error")

            self.labels.append(label)
            field.error_widget = error

            yield label
            yield field.do_render()
            yield field.error_widget

        self.submit = Button(label="Submit", name="submit", classes="green-button")
        self.exit = Button(label="Exit", name="exit", classes="red-button")

        yield self.submit
        yield self.exit

        for field in self.fields:
            yield Static(f"[b][{field.label}][/b] - {field.description}")

    def on_mount(self):
        self.title = "videopy script form"

        for label in self.labels:
            label.styles.padding = 1

        for field in self.fields:
            field.after_render()

        self.submit.styles.margin = 1
        self.exit.styles.margin = 1

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.name == "submit":
            validation = True

            for field in self.fields:
                validation_result = field.validate()

                if not validation_result.is_valid:
                    failures = ""

                    for failure in validation_result.failures:
                        failures += failure.description

                    field.error_widget.update(failures)
                    validation = False
                else:
                    field.error_widget = None

            if validation:
                self.exit()
        elif event.button.name == "exit":
            self.exit()
