import re


RE_PROPERTY = re.compile(r'@(?P<property>\w+)=["\']*(?P<value>\w+)["\']*')
RE_CONTAINS = re.compile(r'contains\(@(?P<property>\w+),[ "\']*(?P<value>\w+)["\']*\)')

CLOSURE = r"</{}>"
