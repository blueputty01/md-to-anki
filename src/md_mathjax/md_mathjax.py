#!/usr/bin/env python
# -*-coding:utf-8-*-

from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension

# inspired by https://github.com/a358003542/md4mathjax

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
    """ """

    def __init__(self, pattern, tag, extension):
        super().__init__(pattern)
        self.extension = extension
        self.tag = tag

    def handleMatch(self, m, data):
        text = m.group("math")
        text = text.replace("}", "} ")

        ret_text = text
        if self.tag == "div":
            ret_text = "\[" + text + "\]"
        else:
            ret_text = "\(" + text + "\)"

        return ret_text, m.start(0), m.end(0)


class Md4MathjaxExtension(Extension):
    """
    A markdown extension enabling mathjax processing in Markdown
    """

    def __init__(self, **kwargs):
        self.config = {
            "auto_insert": [True, "You may insert yourself in another way?"],
            "tag_class": ["math", "The class of the tag in which math is wrapped"],
            "mathjax_settings": [DEFUALT_MATHJAX_SETTING, "mathjax settings"],
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
        mathjax_inline_regex = (
            r"(?<!\$)\$(?!\$)"
            r"(?P<math>.+?)"
            r"(?<!\$)\$(?!\$)"
        )
        mathjax_display_regex = (
            r"(?<!\$)\$\$(?!\$)"
            r"(?P<math>.+?)"
            r"(?<!\$)\$\$(?!\$)"
        )
        md.inlinePatterns.register(
            MathJaxInlinePattern(mathjax_inline_regex, "span", self),
            "mathjax_inlined1",
            190,
        )
        md.inlinePatterns.register(
            MathJaxInlinePattern(mathjax_display_regex, "div", self),
            "mathjax_displayed1",
            182,
        )


def makeExtension(**kwargs):
    return Md4MathjaxExtension(**kwargs)
