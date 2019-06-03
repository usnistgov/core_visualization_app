""" Parser utils test class
"""
from unittest import TestCase

from core_visualization_app.utils import parser


class TestParseCell(TestCase):

    def test_parse_cell_valid(self):
        # Arrange
        value = 'value'
        # Act
        parsed_cell = parser.parse_cell(value)
        result = 'value'
        # Assert
        self.assertTrue(parsed_cell == result)

    def test_parse_cell_multiple(self):
        # Arrange
        value = 'CDCS, ITL, NIST'
        # Act
        parsed_cell = parser.parse_cell(value)
        result = 'CDCS ITL NIST'
        # Assert
        self.assertTrue(parsed_cell == result)

    def test_parse_cell_empty(self):
        # Arrange
        value = ''
        # Act
        parsed_cell = parser.parse_cell(value)
        result = ''
        # Assert
        self.assertTrue(parsed_cell == result)

    def test_parse_cell_unicode(self):
        # Arrange
        value = unicode('unicode')
        # Act
        parsed_cell = parser.parse_cell(value)
        result = 'unicode'
        # Assert
        self.assertTrue(parsed_cell == result)
