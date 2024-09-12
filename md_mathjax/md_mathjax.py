#!/usr/bin/env python
# -*-coding:utf-8-*-

import os
import xml.etree.ElementTree as ET

from markdown.treeprocessors import Treeprocessor
from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension

DEFUALT_MATHJAX_SETTING = r"""
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [["$$", "$$"], ['\\[', '\\]']],
    packages: {
      '[+]': ['mhchem']
    }
  },
  loader: {
    load: ['[tex]/mhchem']
  },
}
"""


class MathJaxInlinePattern(InlineProcessor):
    """
    """

    def __init__(self, pattern, tag, extension):
        super().__init__(pattern)
        self.extension = extension
        self.tag = tag

    def handleMatch(self, m, data):
        el = ET.Element(self.tag)
        el.set('class', self.extension.getConfig('tag_class'))

        if self.tag == 'div':
            el.text = '$$' + m.group('math') + '$$'
        else:
            el.text = '$' + m.group('math') + '$'

        self.extension.mathjax_needed = True

        return el, m.start(0), m.end(0)


class Md4MathjaxExtension(Extension):
    """
    A markdown extension enabling mathjax processing in Markdown
    """

    def __init__(self, **kwargs):
        self.config = {
            "auto_insert": [True,
                            'You may insert yourself in another way?'],
            "tag_class": ["math",
                          "The class of the tag in which math is wrapped"],
            "mathjax_settings": [DEFUALT_MATHJAX_SETTING,
                                 'mathjax settings']
        }
        # mainly set config
        super().__init__(**kwargs)

        # Used as a flag to determine if javascript needs to be injected
        self.mathjax_needed = False

    def reset(self):
        self.mathjax_needed = False

    def extendMarkdown(self, md):
        # later we will use it
        self.md = md

        # Regex to detect mathjax
        mathjax_inline_regex1 = r'(?<!\$)\$(?!\$)' \
                                r'(?P<math>.+?)' \
                                r'(?<!\$)\$(?!\$)'
        mathjax_inline_regex2 = r'\\\((?P<math>.*?)\\\)'

        mathjax_display_regex1 = r'(?<!\$)\$\$(?!\$)' \
                                 r'(?P<math>.+?)' \
                                 r'(?<!\$)\$\$(?!\$)'

        mathjax_display_regex2 = r'\\\[(?P<math>.+?)\\\]'

        md.inlinePatterns.register(
            MathJaxInlinePattern(mathjax_inline_regex1, 'span', self),
            'mathjax_inlined1', 184)

        # must higher than 180 for before the markdown EscapeInlineProcessor
        # and must lower than mathjax_inlined1
        md.inlinePatterns.register(
            MathJaxInlinePattern(mathjax_inline_regex2, 'span', self),
            'mathjax_inlined2', 183)

        md.inlinePatterns.register(
            MathJaxInlinePattern(mathjax_display_regex1, 'div', self),
            'mathjax_displayed1', 182)

        # must higher than 180 for before the markdown EscapeInlineProcessor
        # and must lower than mathjax_inlined1
        md.inlinePatterns.register(
            MathJaxInlinePattern(mathjax_display_regex2, 'div', self),
            'mathjax_displayed', 181)


def makeExtension(**kwargs):
    return Md4MathjaxExtension(**kwargs)