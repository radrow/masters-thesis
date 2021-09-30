"""
    pygments.lexers.sophia
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexer for Sophia language. Modified original JavaScript lexer from pygments.

    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import bygroups, combined, default, do_insertions, include, \
    inherit, Lexer, RegexLexer, this, using, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Other, Generic, Literal
from pygments.util import get_bool_opt
import pygments.unistring as uni

__all__ = ['SophiaLexer']

JS_IDENT_START = ('(?:[$_' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl') +
                  ']|\\\\u[a-fA-F0-9]{4})')
JS_IDENT_PART = ('(?:[$' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl',
                                       'Mn', 'Mc', 'Nd', 'Pc') +
                 '\u200c\u200d]|\\\\u[a-fA-F0-9]{4})')
JS_IDENT = JS_IDENT_START + '(?:' + JS_IDENT_PART + ')*'

line_re = re.compile('.*?\n')

class SophiaLexer(RegexLexer):
    """
    For Sophia source code.
    """

    name = 'Sophia'
    aliases = ['sophia', 'aes']
    filenames = ['*.aes', '*.aci']
    mimetypes = ['application/sophia', 'application/x-sophia',
                 'text/x-sophia', 'text/sophia']

    flags = re.DOTALL | re.UNICODE | re.MULTILINE

    tokens = {
        'commentsandwhitespace': [
            (r'\s+', Text),
            (r'<!--', Comment),
            (r'//.*?\n', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline)
        ],
        'slashstartsregex': [
            include('commentsandwhitespace'),
            (r'/(\\.|[^[/\\\n]|\[(\\.|[^\]\\\n])*])+/'
             r'([gimuysd]+\b|\B)', String.Regex, '#pop'),
            (r'(?=/)', Text, ('#pop', 'badregex')),
            default('#pop')
        ],
        'badregex': [
            (r'\n', Text, '#pop')
        ],
        'root': [
            (r'\A#! ?/.*?\n', Comment.Hashbang),  # recognized by node.js
            (r'^(?=\s|/|<!--)', Text, 'slashstartsregex'),
            include('commentsandwhitespace'),

            # Numeric literals
            (r'0[xX][0-9a-fA-F]+n?', Number.Hex),
            (r'[0-9]+', Number.Integer),

            (r'\.\.\.|=>', Punctuation),
            (r'\+\+|--|~|\?\?=?|\?|:|\\(?=\n)|'
             r'(\'|@|<<|>>>?|==?|!=?|(?:\*\*|\|\||&&|[-<>+*%&|^/]))=?', Operator, 'slashstartsregex'),
            (r'[{(\[;,]', Punctuation, 'slashstartsregex'),
            (r'[})\].]', Punctuation),

            (r'(mod)\b', Operator.Word, 'slashstartsregex'),

            (r'\b(stateful|payable|public|private)\b', Keyword.Reserved),

            (r'\b(true|false)\b', Literal),

            (r'\b(include|compiler|switch|if|elif|else)\b', Keyword, 'slashstartsregex'),
            (r'(let|type|record|datatype|function|entrypoint|contract|namespace|interface)\b', Keyword.Declaration, 'slashstartsregex'),
            (r'(contract|namespace|interface)\b', Keyword.Namespace, 'slashstartsregex'),

            (r'(abort|require|state|put)\b', Keyword.Constant),

            (r'(int|bool|address|string|char|unit)\b', Name.Builtin),

            # Match stuff like: super(argument, list)
            (r'(super)(\s*)(\([\w,?.$\s]+\s*\))',
             bygroups(Keyword, Text), 'slashstartsregex'),
            # Match stuff like: function() {...}
            (r'([a-zA-Z_?.$][\w?.$]*)(?=\(\) \{)', Name.Other, 'slashstartsregex'),

            (JS_IDENT, Name.Other),
            (r'"(\\\\|\\[^\\]|[^"\\])*"', String.Double),
            (r"'(\\\\|\\[^\\]|[^'\\])*'", String.Single),
            (r'`', String.Backtick, 'interp'),
        ],
        'interp': [
        ],
        'interp-inside': [
            # TODO: should this include single-line comments and allow nesting strings?
            (r'\}', String.Interpol, '#pop'),
            include('root'),
        ],
    }

