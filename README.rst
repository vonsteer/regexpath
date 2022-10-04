RegexPath PoC
===================

Proof of Concept for facilitating the creation of xpath-like regex, easily written regex for more efficient web
crawling. The reason this project was created is due to the fact that lxml is by nature, quite slow, specifically the
generation of the ElementTree used.

**Warning: This library is intended mostly as an fun experiment, please do not do use this in production.**

The behaviour should be the following:
'//h3/a' -> '<h3[^>]*>(<a[^>]*>[^<]*<\a>)</h3>'
'//h1[@itemprop="name"]' -> '<h1[^>]*itemprop="name"[^>]*>[^<]*</h1>'
'//a[contains(@class,'checkBookDownloaded')]/@href' -> '<a[^>]*class="[^"]*checkBookDownloaded[^"]*"[^>]*href="([^"]*)">'
'//div[contains(@class,'property_year')]/div[contains(@class,'property_value')]' -> '<div[^>]*class="[^"]*property_year[^"]*"[^>]*><div[^>]*class="[^"]*property_year[^"]*"[^>]*><\div>>'

Singleton elements may pose an issue:
    <area />
    <base />
    <br />
    <col />
    <embed />
    <hr />
    <img />
    <input />
    <link />
    <meta />
    <param />
    <source />
    <track />
    <wbr />


Usage
-----
The idea is that this can library can replace xpath calls to an etree, so instead of lxml_html etree we can use
RegexPath. Calling etree.xpath() will convert the xpath expression into a valid regex designed for html documents
and then process it. For example::

    from regexpath import RegexPath
    test_string = """<script type="text/javascript" src="test_files/typeahead.js"></script>
                    <script type="text/javascript" src="test_files/bootstrap-tagsinput.js"></script>
                    <script type="text/javascript" src="test_files/jquery.js"></script>
                    <script type="text/javascript" src="test_files/z-booklists-carousel.js"></script>
                    <script type="text/javascript" src="test_files/z-readlist-card.js"></script>
                    <script type="text/javascript" src="test_files/book-details.js"></script>"""
    etree = RegexPath(test_string)
    etree.xpath("//script[contains(@src, 'jquery')]")
    >>> '<script type="text/javascript" src="test_files/jquery.js"></script>'
    etree.xpath("//script[contains(@src, 'jquery')]/@src")
    >>> "test_files/jquery.js"


Development
-----------
In order to install development dependencies run::

   pip install -r requirements.txt

In order to run tests locally::

   pytest -k ''

Licence
-------


Authors
-------
`regexpath` was written by `Jesse Constante <jglconstant@gmail.com>`_.
