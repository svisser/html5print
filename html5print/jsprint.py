# -*- coding: utf-8 -*-
#
# Copyright 2014 Bernard Yue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import unicode_literals, absolute_import

import os
import re
import jsbeautifier

from .utils import BeautifierBase


class JSBeautifier(BeautifierBase):
    """Javascript Beautifier - A wrapper class of jsbeautifier"""

    @classmethod
    def beautify(cls, js, indent=2, encoding=None):
        """beautifying javascript `js` by reindending to width of `indent` per
        level.  `js` is expected to be a valid javascript (i.e. no html
        comment(s) tag <!-- ... -->).
        :param js:       a valid javascript as multiline string
        :param encoding: expected encoding of `js`.  If None, it will be
                         guesssed
        :param indent:   width od indentation per level
        :return :        reindented javascript

        >>> from html5print import JSBeautifier

        >>> js = '''function myFunction() {
        ... document.getElementById("demo").innerHTML = "Paragraph changed.";
        ... }'''
        >>> print(JSBeautifier.beautify(js))
        function myFunction() {
          document.getElementById("demo").innerHTML = "Paragraph changed.";
        }

        """
        opts = jsbeautifier.default_options()
        opts.indent_size = indent
        return jsbeautifier.beautify(js, opts)

    @classmethod
    def beautifyTextInHTML(cls, html, indent=2, encoding=None):
        """Beautifying javascript within the <script></script> tag.  Note that
        html comment(s), i.e. <!-- ... --> will be moved to the end of the
        block.
        :param html:      html as string
        :param indent:    width of indentation for embedded javascript in HTML
        :return :         html with javascript beautified (i.e. text
                          within <script>...</script>

        >>> from html5print import JSBeautifier

        >>> js = '''<html><body>
        ...   <script>function myFunction() {
        ... document.getElementById("demo").innerHTML = "Paragraph changed.";
        ... }
        ...   </script>
        ... </body></html>
        ... '''
        >>> print(JSBeautifier.beautifyTextInHTML(js))
        <html><body>
          <script>
            function myFunction() {
              document.getElementById("demo").innerHTML = "Paragraph changed.";
            }
          </script>
        </body></html>
        <BLANKLINE>
        """
        opts = jsbeautifier.default_options()
        opts.indent_size = indent
        return cls.findAndReplace(html, cls.reIndentAndScript,
                                  jsbeautifier.beautify, (opts,), indent)