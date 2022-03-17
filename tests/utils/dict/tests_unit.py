""" Dict utils test class
"""
from unittest import TestCase
from collections import OrderedDict
from core_visualization_app.utils import dict
from os.path import join, dirname, abspath

RESOURCES_PATH = join(dirname(abspath(__file__)), "data")


class TestGetDictValue(TestCase):
    def test_get_dict_value_valid(self):
        # Arrange
        dict_content = {"k": {"e": {"key": 1}}}
        key = "key"
        # Act
        value = dict.get_dict_value(dict_content, key)
        # Assert
        self.assertTrue(value == 1)


class TestGetDictPathValue(TestCase):
    def test_get_dict_path_value_valid(self):
        # Arrange
        dict_content = {
            "amTestDB": {"amTest": {"partTest": {"projectID": "NIST-RPS-14"}}}
        }
        path = "dict_content.amTestDB.amTest.partTest.projectID"
        # Act
        dict_content_path = dict.get_dict_path_value(dict_content, path)
        result = "NIST-RPS-14"
        # Assert
        self.assertTrue(dict_content_path == result)


class TestGetTestTypeTree(TestCase):
    def test_get_test_type_tree_valid(self):
        # Arrange
        all_tree = {
            "annotations": {},
            "children": OrderedDict(
                [
                    (
                        "http://siam.nist.gov/Database-Navigation-Ontology#BulkDensity",
                        {
                            "annotations": {
                                "filter": '{ "dict_content.amTestDB.amTest.partTest.testType": "BULKDENSITY" }',
                                "visualization": '["title": "Data table"}]',
                            }
                        },
                    ),
                    (
                        "http://siam.nist.gov/Database-Navigation-Ontology#GrainSize",
                        {
                            "annotations": {
                                "filter": '{ "dict_content.amTestDB.amTest.partTest.testType": "GRAIN" }',
                                "visualization": '[{"title": "Data table"}]',
                            }
                        },
                    ),
                    (
                        "http://siam.nist.gov/Database-Navigation-Ontology#Tensile",
                        {
                            "annotations": {
                                "filter": '{ "dict_content.amTestDB.amTest.partTest.testType": "TENSILE" }',
                                "visualization": '[{"title": "Data table"}]',
                            }
                        },
                    ),
                ]
            ),
        }
        test_type_name = "Tensile"
        # Act
        test_type_tree = dict.get_test_type_tree(all_tree, test_type_name)
        expected_result = {
            "annotations": {
                "filter": '{ "dict_content.amTestDB.amTest.partTest.testType": "TENSILE" }',
                "visualization": '[{"title": "Data table"}]',
            }
        }
        # Assert
        self.assertTrue(test_type_tree == expected_result)


class TestGetListInsideDict(TestCase):
    def test_get_list_inside_dict_valid_multi(self):
        # Arrange
        dict_path = "dict_content.amTestDB.amTest.partTest.testResults.chemistry.constituent.element"
        dict_content = {
            "amTestDB": {
                "amTest": {
                    "partTest": {
                        "testResults": {
                            "chemistry": {
                                "constituent": [
                                    {"element": "Oxygen"},
                                    {"element": "Carbon"},
                                    {"element": "Nitrogen"},
                                    {"element": "Sulfur"},
                                    {"element": "Manganese"},
                                    {"element": "Silicon"},
                                    {"element": "Phosphorus"},
                                    {"element": "Chromium"},
                                    {"element": "Molybdenum"},
                                    {"element": "Niobium"},
                                    {"element": "Tantalum"},
                                    {"element": "Cobalt"},
                                    {"element": "Titanium"},
                                    {"element": "Aluminum"},
                                    {"element": "Iron"},
                                ]
                            }
                        }
                    }
                }
            }
        }
        # Act
        list_inside_dict = dict.get_list_inside_dict(dict_path, dict_content)
        result = [
            {"element": "Oxygen"},
            {"element": "Carbon"},
            {"element": "Nitrogen"},
            {"element": "Sulfur"},
            {"element": "Manganese"},
            {"element": "Silicon"},
            {"element": "Phosphorus"},
            {"element": "Chromium"},
            {"element": "Molybdenum"},
            {"element": "Niobium"},
            {"element": "Tantalum"},
            {"element": "Cobalt"},
            {"element": "Titanium"},
            {"element": "Aluminum"},
            {"element": "Iron"},
        ]
        # Assert
        self.assertTrue(list_inside_dict == result)

    def test_get_list_inside_dict_valid_simple(self):
        # Arrange
        dict_path = "dict_content.amTestDB.amTest.partTest.testResults.chemistry.constituent.element"
        dict_content = {
            "amTestDB": {
                "amTest": {
                    "partTest": {
                        "testResults": {
                            "chemistry": {"constituent": [{"element": "Iron"}]}
                        }
                    }
                }
            }
        }
        # Act
        list_inside_dict = dict.get_list_inside_dict(dict_path, dict_content)
        result = [{"element": "Iron"}]
        # Assert
        self.assertTrue(list_inside_dict == result)

    def test_get_list_inside_dict_none(self):
        # Arrange
        dict_path = "dict_content.amTestDB.amTest.partTest.testResults.chemistry.constituent.element"
        dict_content = {"amTestDB": {"amTest": {"partTest": {"testResults": {}}}}}
        # Act
        list_inside_dict = dict.get_list_inside_dict(dict_path, dict_content)
        # Assert
        self.assertIsNone(list_inside_dict)


class TestGetDictsInsideListOfDict(TestCase):
    def test_get_dicts_inside_list_of_dict_valid(self):
        # Arrange
        list_path = ["a", "b", "c"]
        list_of_dict = [
            {"a": {"b": {"c": "value1"}}},
            {"a": {"b": {"c": "value2"}}},
            {"a": {"b": {"c": "value3"}}},
        ]
        # Act
        dicts_inside_list_of_dicts = dict.get_dicts_inside_list_of_dict(
            list_path, list_of_dict
        )
        # Assert
        self.assertTrue(
            dicts_inside_list_of_dicts
            == [{"c": "value1"}, {"c": "value2"}, {"c": "value3"}]
        )


class TestGetChildrenTrees(TestCase):
    def test_get_children_trees_valid(self):
        # Arrange
        tree = OrderedDict(
            [
                (
                    "http://siam.nist.gov/Database-Navigation-Ontology#ChemicalComposition",
                    {
                        "annotations": {
                            "filter": '{  "dict_content.amTestDB.amTest.powderTest.testType": "CHEMISTRY-XPS" }',
                            "visualization": "[{'title': 'Data table'}, 'children': OrderedDict()]",
                        }
                    },
                ),
                (
                    "http://siam.nist.gov/Database-Navigation-Ontology#Microstructure",
                    {
                        "annotations": {
                            "filter": '{  "dict_content.amTestDB.amTest.powderTest.testType": "MICROSTRUCTURE-XRD" }',
                            "visualization": "[{'title': 'Data table'}, 'children': OrderedDict()]",
                        }
                    },
                ),
                (
                    "http://siam.nist.gov/Database-Navigation-Ontology#ParticleSize",
                    {
                        "annotations": {
                            "filter": '{  "dict_content.amTestDB.amTest.powderTest.testType": "PARTICLESIZE-PSD" }',
                            "visualization": "[{'title': 'Data table'}, 'children': OrderedDict()]",
                        }
                    },
                ),
            ]
        )
        # Act
        children_trees = dict.get_children_trees(tree)
        expected_result = [
            {
                "ChemicalComposition": {
                    "annotations": {
                        "filter": '{  "dict_content.amTestDB.amTest.powderTest.testType": "CHEMISTRY-XPS" }',
                        "visualization": "[{'title': 'Data table'}, 'children': OrderedDict()]",
                    }
                }
            },
            {
                "Microstructure": {
                    "annotations": {
                        "filter": '{  "dict_content.amTestDB.amTest.powderTest.testType": "MICROSTRUCTURE-XRD" }',
                        "visualization": "[{'title': 'Data table'}, 'children': OrderedDict()]",
                    }
                }
            },
            {
                "ParticleSize": {
                    "annotations": {
                        "filter": '{  "dict_content.amTestDB.amTest.powderTest.testType": "PARTICLESIZE-PSD" }',
                        "visualization": "[{'title': 'Data table'}, 'children': OrderedDict()]",
                    }
                }
            },
        ]
        # Assert
        self.assertTrue(children_trees == expected_result)


class TestCheckChildren(TestCase):
    def test_check_children_No_Children(self):
        # Arrange
        tree = {"NoChildren": {"Imbricatedkey": "AMMD"}}
        # Act
        expected_result = [{"NoChildren": {"Imbricatedkey": "AMMD"}}]
        # Assert
        self.assertTrue(dict.check_children(tree) == expected_result)

    def test_check_children_With_Children(self):
        # Arrange
        tree = {
            "ImaParent": {
                "children": {
                    "http://siam.nist.gov/Database-Navigation-Ontology#Child": {
                        "ToReturn": "a"
                    },
                    "http://siam.nist.gov/Database-Navigation-Ontology#OtherChild": {
                        "ToReturn": "b"
                    },
                },
                "NotChild": {"DoNot": "Return"},
            }
        }
        # Act
        expected_result = [
            {"OtherChild": {"ToReturn": "b"}},
            {"Child": {"ToReturn": "a"}},
        ]
        # Assert
        self.assertTrue(dict.check_children(tree) == expected_result)
