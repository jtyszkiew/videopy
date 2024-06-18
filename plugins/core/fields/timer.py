from textual.app import ComposeResult
from textual.widgets import Static, Input
from textual.widget import Widget
from textual.containers import Horizontal

from videopy.form import AbstractField, AbstractFieldFactory


class Timer(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hours = Input(placeholder="HH", name="hours", type="number")
        self.minutes = Input(placeholder="MM", name="minutes", type="number")
        self.seconds = Input(placeholder="SS", name="seconds", type="number")
        self.horizontal = Horizontal()

    def compose(self) -> ComposeResult:
        self.hours.styles.width = 9
        self.minutes.styles.width = 9
        self.seconds.styles.width = 9

        with self.horizontal:
            yield self.hours
            yield self.minutes
            yield self.seconds

    def combine_time(self) -> str:
        try:
            h = int(self.hours.value) if self.hours.value else 0
            m = int(self.minutes.value) if self.minutes.value else 0
            s = int(self.seconds.value) if self.seconds.value else 0
            total_seconds = h * 3600 + m * 60 + s
            return f"{h:02}:{m:02}:{s:02} ({total_seconds} seconds)"
        except ValueError:
            return "Invalid input!"

    def get_combined_time(self) -> int:
        """Returns the combined time in seconds."""
        try:
            h = int(self.hours.value) if self.hours.value else 0
            m = int(self.minutes.value) if self.minutes.value else 0
            s = int(self.seconds.value) if self.seconds.value else 0
            return h * 3600 + m * 60 + s
        except ValueError:
            return None


class Field(AbstractField):
    def __init__(self, form, field_type, name, label, configuration, required, description=""):
        super().__init__(form, field_type, name, label, required, description)
        self.configuration = configuration

    def render(self):
        return Timer()

    def after_render(self):
        self.widget.styles.height = 3

    def get_value(self):
        return {
            "hours": self.widget.hours.value,
            "minutes": self.widget.minutes.value,
            "seconds": self.widget.seconds.value,
            "combined_time_in_seconds": self.widget.get_combined_time(),
        }


class FieldFactory(AbstractFieldFactory):
    def from_yml(self, field_yml, name, form):
        configuration = field_yml['configuration'] if 'configuration' in field_yml else {}

        return Field(form, field_yml['type'], name, field_yml['label'], configuration, field_yml['required'],
                     field_yml.get('description', ''))
