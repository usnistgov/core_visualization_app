"""
Selected Test models
"""

from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors

from core_main_app.commons import exceptions


class SelectedTest(Document):
    """Data Structure to handle the selected test (ie. subcategory)"""

    name = fields.StringField(blank=True)
    is_selected = fields.BooleanField(default=False)
    category = fields.StringField(blank=True)

    @staticmethod
    def create_selected(selected_name):
        """Create and return a selected test

        Args:
            selected_name:

        Returns:

        """
        selected_test = SelectedTest.objects.create(name=selected_name)
        return selected_test

    @staticmethod
    def toggle_test_selection(selected_test_name):
        """Toggle the test selection. Only one test can be selected at the same time, all the other selected test are
        updated as 'is selected' = False while the one corresponding
        to the given test name 'is selected' field is updated as True.

        Args:
            selected_test_name:

        Returns:

        """
        SelectedTest.objects.all().update(is_selected=False)
        SelectedTest.objects.filter(name=selected_test_name).update(is_selected=True)

    @staticmethod
    def get_selected_test():
        """Return the selected test whose 'is selected' field is True

        Returns:

        """
        try:
            return SelectedTest.objects.filter(is_selected=True)[0]
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))
