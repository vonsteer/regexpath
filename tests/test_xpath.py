import unittest

from tests import base


class BasicUnitTest(base.TestBase, unittest.TestCase):
    """Tests simple xpath expressions."""

    expected_output = [
        '<a href="https://ar.1lib.limited/book/974906/328248" style="text-decoration: underline;">Garlic and Oil: Politics and Food in Italy</a>',
        '<a href="https://ar.1lib.limited/book/974904/68e17c" style="text-decoration: underline;">The 1970s is Here and Now (Architectural Design 03-04.2005, Vol. 75, No. 2)</a>',
    ]
    xpath_expression = "//h3/a"


class PropertyUnitTest(BasicUnitTest):
    """Tests the conversion of xpath expressions that contain property specifications."""

    expected_output = [
        '<h1 itemprop="name" style="color: #000; line-height: 140%;">\n                Islamic Codicology: An Introduction to the Study of Manuscripts in Arabic Script            </h1>'
    ]
    xpath_expression = '//h1[@itemprop="name"]'


class ContainsUnitTest(BasicUnitTest):
    """Tests the conversion of more complex xpath expressions."""

    expected_output = [
        "https://ar.1lib.limited/apple-touch-icon.png?v=1",
        "https://ar.1lib.limited/favicon.svg",
        "https://ar.1lib.limited/favicon-32x32.svg?v=2",
        "https://ar.1lib.limited/favicon-16x16.svg?v=2",
        "https://ar.1lib.limited/safari-pinned-tab.svg?v=1",
    ]
    xpath_expression = "//link[contains(@rel,'icon')]/@href"


class Contains2UnitTest(BasicUnitTest):
    """Tests the conversion of more complex xpath expressions."""

    expected_output = [
        '<div class="property_label">عام:</div>\n            <div class="property_value ">2006</div>',
        '<div class="property_label">عام:</div>\n            <div class="property_value ">2004</div>',
        '<div class="property_label">عام:</div>\n            <div class="property_value ">2005</div>',
    ]
    xpath_expression = "//div[contains(@class,'property_year')]/div[contains(@class,'property_label')]"
