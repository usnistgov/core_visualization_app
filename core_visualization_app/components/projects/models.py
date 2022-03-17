"""
projects models
"""


from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors

from core_main_app.commons import exceptions


class Projects(Document):
    """Data Structure to handle the selected projects"""

    name = fields.StringField(blank=True)
    is_selected = fields.BooleanField(default=False)

    @staticmethod
    def create_project(project_name):
        """Create project with the given argument as project name and return the project

        Args:
            project_name:

        Returns:

        """
        project = Projects.objects.create(name=project_name)
        return project

    @staticmethod
    def get_project_by_name(project_name):
        """Return the project with the given name

        Args:
            project_name:

        Returns:

        """
        return Projects.objects.get(name=project_name)

    @staticmethod
    def toggle_project_selection(project_name, selection):
        """Toggle the boolean that indicates if a project is selected or not.
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
        """Return the list of all the projects names whose 'is_selected' is True

        Returns:

        """
        try:
            selected_projects = Projects.objects.filter(is_selected=True)
            selected_projects_name = []
            for selected_project in selected_projects:
                selected_projects_name.append(selected_project.name)
            return selected_projects_name

        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def delete_all_projects():
        """Delete all projects

        Returns:

        """
        Projects.objects.all().delete()
