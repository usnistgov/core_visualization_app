""" Visualization Selection models
"""

import json

from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors

import core_explore_tree_app.components.data.query as query_database_api
import core_explore_tree_app.parser.parser as ontology_parser
from core_main_app.commons import exceptions
from core_visualization_app.components.visualization_selection import operations
from core_visualization_app.utils import dict as dict_utils

CQL_NAMESPACE = "http://siam.nist.gov/Database-Navigation-Ontology#"


class Projects(Document):
    """ Data Structure to handle the selected projects
    """
    name = fields.StringField(blank=True)
    is_selected = fields.BooleanField(default=False)

    @staticmethod
    def create_project(project_name):
        """ Create project with the given argument as project name and return the project

        Args:
            project_name:

        Returns:

        """
        project = Projects.objects.create(name=project_name)
        return project

    @staticmethod
    def get_project_by_name(project_name):
        """ Return the project with the given name

        Args:
            project_name:

        Returns:

        """
        return Projects.objects.get(name=project_name)

    @staticmethod
    def toggle_project_selection(project_name, selection):
        """ Toggle the boolean that indicates if a project is selected or not.
        Return the project with the given project name

        Args:
            project_name:
            selection:

        Returns:

        """
        Projects.objects.filter(name=project_name).update(is_selected=not selection)
        return Projects.objects.get(name=project_name)

    @staticmethod
    def get_selected_projects_name():
        """ Return the list of all the projects names whose 'is_selected' is True

        Returns:

        """
        try:
            selected_projects = Projects.objects.filter(is_selected=True)
            selected_projects_name = []
            for selected_project in selected_projects:
                selected_projects_name.append(selected_project.name)
            return selected_projects_name

        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as ex:
            raise exceptions.ModelError(ex.message)

    @staticmethod
    def delete_all_projects():
        """ Delete all projects

        Returns:

        """
        Projects.objects.all().delete()

    @staticmethod
    def get_projects(navigation, template_id):
        """ Get all the existing projects from the database

        :param navigation:
        :param template_id:
        :return: list of tuples. Each tuple is a project written twice to be consistent with form syntax
        """
        # Get the filter related to the projects
        owl_node_project = CQL_NAMESPACE + 'AMProject'
        navigation_projects = navigation.get_by_name(owl_node_project)

        projects_id = []

        # All the navigation objects are identical so it is enough to get the information we need from the first one
        if 'filter' in navigation_projects[0].options and navigation_projects[0].options['filter'] is not None:
            project_filter = navigation_projects[0].options['filter']
        if 'projection' in navigation_projects[0].options and navigation_projects[0].options['projection'] is not None:
            project_projection = navigation_projects[0].options['projection']

        if not (project_filter and project_projection is None):
            projects = query_database_api.execute_query(template_id, [project_filter], project_projection)
            for project in projects:
                project_id = dict_utils.get_dict_value(project.dict_content, 'projectID')
                if project_id not in projects_id:
                    Projects.create_project(project_id)
                    projects_id.append(project_id)

        projects_id_tuples = []
        for project_id in projects_id:
            projects_id_tuples.append((project_id, project_id))

        return projects_id_tuples

    @staticmethod
    def get_all_projects_list(navigation, template_id):
        """ Return the list of the projects names tuples to put in the Django forms

        Args:
            navigation:
            template_id:

        Returns:

        """
        projects_id_tuples = Projects.get_projects(navigation, template_id)
        all_projects_list = []
        for project_tuple in projects_id_tuples:
            all_projects_list.append(project_tuple[0])
        return all_projects_list


class Category(Document):
    """Data Structure to handle the selected Category

    """
    name = fields.StringField(blank=True)
    is_selected = fields.BooleanField(default=False)
    subcategories = fields.StringField(blank=True)

    @staticmethod
    def get_all_categories_names():
        """ Return the list of all the categories names

        Returns:

        """
        categories_names = []
        for category in Category.objects.all():
            categories_names.append(category.name)

    @staticmethod
    def create_category(category):
        """ Create and return a Category object

        Args:
            category:

        Returns:

        """
        return Category.objects.create(name=category)

    @staticmethod
    def get_category_by_name(category_name):
        """ Return the category object with the given argument

        Args:
            category_name:

        Returns:

        """
        return Category.objects.get(name=category_name)

    @staticmethod
    def get_selected_category_name():
        """ Return the only one selected category object name

        Returns:

        """
        selected_category = Category.objects.get(is_selected=True)
        return selected_category.name

    @staticmethod
    def toggle_category_selection(category_name):
        """ Toggle the boolean that indicates if a category is selected or not.
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
        """ Return the subcategories list belonging to the given category

        Args:
            category:

        Returns:

        """
        category_tree = operations.get_category_tree(category.name)
        subcategories_list = operations.get_subcategories_list(category_tree)
        Category.objects.filter(name=category.name).update(subcategories=json.dumps(subcategories_list))
        return subcategories_list

    @staticmethod
    def get_categories(active_ontology):
        """ Return category tuples, a list of tuples. Each tuple is a category.
         Return also categories tree, a list of dict. Each dict contains the ontology annotation part related
         to the category which is at the same index within the category tuples.

        :param active_ontology:
        :return:
        """
        tree = ontology_parser.parse_ontology(active_ontology.content)
        owl_node_categories = CQL_NAMESPACE + 'AMTests'
        Category.objects.all().delete()
        categories_tree = []
        categories_tuples = []

        for k, v in tree.items():
            if k == owl_node_categories:
                for k2, v2 in v.items():
                    if k2 == 'children':
                        for k3, v3 in v2.items():
                            category = k3.split(CQL_NAMESPACE)[1]
                            Category.create_category(category)
                            categories_tuples.append((category, category))
                            categories_tree.append(v3)

        return categories_tuples, categories_tree

    @staticmethod
    def get_subcategories_tuples(categories, categories_tree):
        """ Get all the existing categories subclasses (ie. subcategories) from the active ontology as a list of tuples

        :param categories (Build and powder only for now)
        :param categories_tree (ordereddict of each category)
        :return: list of list of tuples. Each tuple is a subclass of a category (ie. a subcategory) and a list gathers all
        the subclasses of a single category. There are as many lists as categories
        """
        subcategories_tuples_list = ()
        i = 0
        for category_tree in categories_tree:
            category = categories[i]
            subcategories = []
            i += 1
            for k, v in category_tree.items():
                if k == 'children':
                    for k2, v2 in v.items():
                        if k2.startswith(CQL_NAMESPACE):
                            subcategory = k2.split(CQL_NAMESPACE)[1]
                            subcategories.append((subcategory, subcategory))
                        bool = False
                        for k3, v3 in v2.items():
                            if k3 == 'children':
                                for k4, v4 in v3.items():
                                    if k4.startswith(CQL_NAMESPACE) and not bool:
                                        bool = True
                                        subcategories.remove((subcategory, subcategory))
                                    if k4.startswith(CQL_NAMESPACE):
                                        subcategory = k4.split(CQL_NAMESPACE)[1]
                                        subcategories.append((subcategory, subcategory))
                    subcategories_tuples_list += (category, subcategories)

        return subcategories_tuples_list

    @staticmethod
    def get_selected_category():
        """ Return the selected category

        Returns:

        """
        try:
            return Category.objects.get(is_selected=True)
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as ex:
            raise exceptions.ModelError(ex.message)


class SelectedTest(Document):
    """Data Structure to handle the selected test (ie. subcategory)

    """
    name = fields.StringField(blank=True)
    is_selected = fields.BooleanField(default=False)
    category = fields.StringField(blank=True)

    @staticmethod
    def create_selected(selected_name):
        """ Create and return a selected test

        Args:
            selected_name:

        Returns:

        """
        selected_test = SelectedTest.objects.create(name=selected_name)
        return selected_test

    @staticmethod
    def toggle_test_selection(selected_test_name):
        """ Toggle the test selection. Only one test can be selected at the same time, all the other selected test are
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
        """ Return the selected test whose 'is selected' field is True

        Returns:

        """
        try:
            return SelectedTest.objects.filter(is_selected=True)[0]
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as ex:
            raise exceptions.ModelError(ex.message)
