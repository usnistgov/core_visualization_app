"""
Category models
"""

import json

from django_mongoengine import fields, Document
from core_visualization_app.components.category import operations


class Category(Document):
    """Data Structure to handle the selected Category"""

    name = fields.StringField(blank=True)
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
