"""
Category models
"""

import json

from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors

from core_main_app.commons import exceptions
from core_visualization_app.components.category import operations


class Category(Document):
    """Data Structure to handle the selected Category"""

    name = fields.StringField(blank=True)
    is_selected = fields.BooleanField(default=False)
    subcategories = fields.StringField(blank=True)

    @staticmethod
    def get_all_categories_names():
        """Return the list of all the categories names

        Returns:

        """
        return Category.objects.all().values_list("name")

    @staticmethod
    def create_category(category):
        """Create and return a Category object

        Args:
            category:

        Returns:

        """
        return Category.objects.create(name=category)

    @staticmethod
    def get_category_by_name(category_name):
        """Return the category object with the given argument

        Args:
            category_name:

        Returns:

        """
        return Category.objects.get(name=category_name)

    @staticmethod
    def get_selected_category_name():
        """Return the only one selected category object name

        Returns:

        """
        selected_category = Category.objects.get(is_selected=True)
        return selected_category.name

    @staticmethod
    def toggle_category_selection(category_name):
        """Toggle the boolean that indicates if a category is selected or not.
        Return the category with the given category name

        Args:
            category_name:

        Returns:

        """
        for category in Category.objects.all():
            if category.name == category_name:
                Category.objects.filter(name=category.name).update(is_selected=True)
            else:
                Category.objects.filter(name=category.name).update(is_selected=False)

        return Category.objects.get(name=category_name)

    @staticmethod
    def get_subcategories(category):
        """Return the subcategories list belonging to the given category

        Args:
            category:

        Returns:

        """
        category_tree = operations.get_category_tree(category.name)
        subcategories_list = operations.get_subcategories_list(
            [category.name], [category_tree]
        )
        Category.objects.filter(name=category.name).update(
            subcategories=json.dumps(subcategories_list)
        )
        return subcategories_list

    @staticmethod
    def delete_all_categories():
        """Delete all category objects

        Returns:

        """
        Category.objects.all().delete()

    @staticmethod
    def get_selected_category():
        """Return the selected category

        Returns:

        """
        try:
            return Category.objects.get(is_selected=True)
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))
