import unittest
from unittest.mock import MagicMock
from textual.validation import ValidationResult
from textual.widgets import Static

from videopy.form import AbstractField, Form


class TestAbstractField(unittest.TestCase):

    def setUp(self):
        self.form = MagicMock()
        self.field = AbstractField(self.form, 'text', 'name', 'Name', required=True)

        self.field.widget = MagicMock()
        self.field.widget.value = "some value"
        self.field.widget.validate = MagicMock(return_value=ValidationResult.success())

    def test_validate_success(self):
        result = self.field.validate()
        self.assertTrue(result.is_valid)

    def test_validate_no_validate_method(self):
        del self.field.widget.validate
        result = self.field.validate()
        self.assertTrue(result.is_valid)


class TestForm(unittest.TestCase):

    def setUp(self):
        self.app = Form()
        self.field = MagicMock(spec=AbstractField)
        self.field.label = "Test Label"
        self.field.do_render = MagicMock(return_value=Static("Test Widget"))
        self.field.validate = MagicMock(return_value=ValidationResult.success())
        self.app.add_field(self.field)

    def test_add_field(self):
        self.assertIn(self.field, self.app.fields)
