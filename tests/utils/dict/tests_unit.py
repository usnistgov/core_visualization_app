""" Dict utils test class
"""
from unittest import TestCase
from collections import OrderedDict
from core_visualization_app.utils import dict
from os.path import join, dirname, abspath

RESOURCES_PATH = join(dirname(abspath(__file__)), 'data')


class TestGetDictValue(TestCase):

    def test_get_dict_value_valid(self):
        # Arrange
        dict_content = {'k': {'e': {'key': 1}}}
        key = 'key'
        # Act
        value = dict.get_dict_value(dict_content, key)
        # Assert
        self.assertTrue(value == 1)


class TestGetDictPathValue(TestCase):

    def test_get_dict_path_value_valid(self):
        # Arrange
        dict_content = {u'amTestDB': {u'amTest': {u'partTest': {u'projectID': u'NIST-RPS-14'}}}}
        path = 'dict_content.amTestDB.amTest.partTest.projectID'
        # Act
        dict_content_path = dict.get_dict_path_value(dict_content, path)
        result = 'NIST-RPS-14'
        # Assert
        self.assertTrue(dict_content_path == result)


class TestGetTestTypeTree(TestCase):

    def test_get_test_type_tree_valid(self):
        # Arrange
        all_tree_file = open(join(RESOURCES_PATH, 'test_type_all_tree.txt'), "r")
        all_tree = OrderedDict(all_tree_file.read())
        test_type_name = 'Tensile'
        # Act
        test_type_tree = dict.get_test_type_tree(all_tree, test_type_name)
        expected_result_file = open(join(RESOURCES_PATH, 'test_type_category_tree.txt'), "r")
        expected_result = OrderedDict(expected_result_file.read())
        # Assert
        self.assertTrue(test_type_tree == expected_result)


class TestGetListInsideDict(TestCase):

    def test_get_list_inside_dict_valid_multi(self):
        # Arrange
        dict_path = 'dict_content.amTestDB.amTest.partTest.testResults.chemistry.constituent.element'
        dict_content = {u'amTestDB': {u'amTest': {u'partTest': {u'testResults': {u'chemistry': {u'constituent': [{u'element': u'Oxygen'}, {u'element': u'Carbon'}, {u'element': u'Nitrogen'}, {u'element': u'Sulfur'}, {u'element': u'Manganese'}, {u'element': u'Silicon'}, {u'element': u'Phosphorus'}, {u'element': u'Chromium'}, {u'element': u'Molybdenum'}, {u'element': u'Niobium'}, {u'element': u'Tantalum'}, {u'element': u'Cobalt'}, {u'element': u'Titanium'}, {u'element': u'Aluminum'}, {u'element': u'Iron'}]}}}}}}
        # Act
        list_inside_dict = dict.get_list_inside_dict(dict_path, dict_content)
        result = [{u'element': u'Oxygen'}, {u'element': u'Carbon'}, {u'element': u'Nitrogen'}, {u'element': u'Sulfur'}, {u'element': u'Manganese'}, {u'element': u'Silicon'}, {u'element': u'Phosphorus'}, {u'element': u'Chromium'}, {u'element': u'Molybdenum'}, {u'element': u'Niobium'}, {u'element': u'Tantalum'}, {u'element': u'Cobalt'}, {u'element': u'Titanium'}, {u'element': u'Aluminum'}, {u'element': u'Iron'}]
        # Assert
        self.assertTrue(list_inside_dict == result)

    def test_get_list_inside_dict_valid_simple(self):
        # Arrange
        dict_path = 'dict_content.amTestDB.amTest.partTest.testResults.chemistry.constituent.element'
        dict_content = {u'amTestDB': {u'amTest': {u'partTest': {u'testResults': {u'chemistry': {u'constituent': [{u'element': u'Iron'}]}}}}}}
        # Act
        list_inside_dict = dict.get_list_inside_dict(dict_path, dict_content)
        result = [{u'element': u'Iron'}]
        # Assert
        self.assertTrue(list_inside_dict == result)

    def test_get_list_inside_dict_none(self):
        # Arrange
        dict_path = 'dict_content.amTestDB.amTest.partTest.testResults.chemistry.constituent.element'
        dict_content = {u'amTestDB': {u'amTest': {u'partTest': {u'testResults': {}}}}}
        # Act
        list_inside_dict = dict.get_list_inside_dict(dict_path, dict_content)
        # Assert
        self.assertIsNone(list_inside_dict)


class TestGetDictsInsideListOfDict(TestCase):

    def test_get_dicts_inside_list_of_dict_valid(self):
        # Arrange
        list_path = ['a', 'b', 'c']
        list_of_dict = [{'a': {'b': {'c': 'value1'}}}, {'a': {'b': {'c': 'value2'}}}, {'a': {'b': {'c': 'value3'}}}]
        # Act
        dicts_inside_list_of_dicts = dict.get_dicts_inside_list_of_dict(list_path, list_of_dict)
        # Assert
        self.assertTrue(dicts_inside_list_of_dicts == [{'c': 'value1'}, {'c': 'value2'}, {'c': 'value3'}])


class TestGetChildrenTrees(TestCase):

    def test_get_children_trees_valid(self):
        # Arrange
        tree_file = open(join(RESOURCES_PATH, 'test_children_tree.txt'), "r")
        tree = OrderedDict(tree_file)
        # Act
        children_trees = dict.get_children_trees(tree)
        expected_result_file = open(join(RESOURCES_PATH, 'test_children_result.txt'), "r")
        expected_result = list(expected_result_file.read())
        # Assert
        self.assertTrue(children_trees == expected_result)


class TestCheckChildren(TestCase):

    def test_check_children_valid(self):
        # Arrange
        tree_file = open(join(RESOURCES_PATH, 'test_check_children.txt'), "r")
        tree = OrderedDict(tree_file.read())
        # Act
        expected_result_file = open(join(RESOURCES_PATH, 'test_check_children_result.txt'), "r")
        expected_result = list(expected_result_file.read())
        # Assert
        self.assertTrue(dict.check_children(tree) == expected_result)


