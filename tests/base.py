import os

from regexpath import regexpath

from lxml import html as lxml_html


class TestBase:
    base_path = os.path.join(os.path.dirname(__file__))
    fixture_name = "test.html"
    expected_output = []
    xpath_expression = ""

    def open_fixture(self, fixture_name: str) -> str:
        with open(f"{self.base_path}/fixtures/{fixture_name}", "r") as file:
            text = file.read()
        return text

    def actual_xpath(self):
        tree = lxml_html.parse(f"{self.base_path}/fixtures/{self.fixture_name}")
        results = tree.xpath(self.xpath_expression)
        if isinstance(results[0], str):
            return results
        output = [lxml_html.tostring(result) for result in tree.xpath(self.xpath_expression)]
        return output

    def regex_path(self):
        data = self.open_fixture(self.fixture_name)
        tree = regexpath.RegexPath(data)
        return tree.xpath(self.xpath_expression)

    def test_parser(self) -> None:
        output = self.regex_path()
        self.assertEqual(output, self.expected_output)
        # For now we need to find ways to make the parser more efficient before adding performance checks
        # regex_time = timeit.timeit(str(self.regex_path()), number=100000)
        # xpath_time = timeit.timeit(str(self.actual_xpath()), number=100000)
        # print(regex_time, xpath_time)
        # self.assertGreater(xpath_time, regex_time)
