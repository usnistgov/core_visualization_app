""" Visualization data model """

from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors


class DataLine(Document):
    """
    data : dict with keys = param name, value = value
    test_type : to call all the line related to a selected test
    id : a doc ID
    project_id : used to know what line are to display according to user selection
    """

    test_type = fields.StringField(blank=False)
    project_id = fields.StringField(blank=False)
    doc_id = fields.StringField(blank=False)
    data = fields.DictField(blank=True, default={})

    @staticmethod
    def delete_all():
        """Delete all the DataLine objects

        Returns:

        """
        all_data_lines = DataLine.objects.all()
        return all_data_lines.delete()

    @staticmethod
    def create_line(test_type, project_id, doc_id):
        """If DataLine already exists we get it, otherwise it is created and saved.
        Returns the DataLine

        Args:
            test_type:
            project_id:
            doc_id:

        Returns:

        """
        doc_id = str(doc_id)
        project_id = str(project_id)

        try:
            data_line = DataLine.objects.get(
                test_type=test_type, project_id=project_id, doc_id=doc_id
            )
            data_line.data = {}
        except mongoengine_errors.DoesNotExist as e:
            data_line = DataLine(
                test_type=test_type, project_id=project_id, doc_id=doc_id
            )

        return data_line.save()

    @staticmethod
    def is_line(doc_id):
        """Return True if a DataLine exists that gets the given argument as doc_id

        Args:
            doc_id:

        Returns:

        """
        doc_id = str(doc_id)
        if DataLine.objects.filter(doc_id=doc_id):
            return True
        return False

    @staticmethod
    def update_line(test_type, project_id, doc_id, param, value):
        """Update a DataLine and return the updated DataLine

        Args:
            test_type:
            project_id:
            doc_id:
            param:
            value:

        Returns:

        """
        # Get the existing data line data
        doc_id = str(doc_id)
        data_line = DataLine.objects.get(
            test_type=test_type, project_id=project_id, doc_id=doc_id
        )
        data_dict = data_line.data

        # Define the new data
        data_new_element = {param: value}
        data_dict.update(data_new_element)

        # Update the database
        DataLine.objects.filter(pk=data_line.pk).update(data=data_dict)

        return data_line

    @staticmethod
    def get_lines(test_type, projects_list):
        """Return the list of all the DataLine data related to a test type and a projects list

        Args:
            test_type:
            projects_list:

        Returns:

        """
        lines = []
        for project in projects_list:
            data_lines = DataLine.objects.filter(
                test_type=test_type, project_id=project
            )
            for data_line in data_lines:
                lines.append(data_line.data)
        return lines
