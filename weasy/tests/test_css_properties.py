# coding: utf8

#  WeasyPrint converts web documents (HTML, CSS, ...) to PDF.
#  Copyright (C) 2011  Simon Sapin
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import attest
from attest import Tests, assert_hook
from cssutils.css import PropertyValue, CSSStyleDeclaration

from ..css.shorthands import expand_shorthand, expand_name_values


suite = Tests()


def expand_to_dict(css):
    """Helper to test shorthand properties expander functions."""
    return dict((name, ' '.join(value.cssText for value in values))
                for prop in CSSStyleDeclaration(css)
                for name, values in expand_shorthand(prop))


@suite.test
def test_expand_four_sides():
    assert expand_to_dict('margin: inherit') == {
        'margin-top': 'inherit',
        'margin-right': 'inherit',
        'margin-bottom': 'inherit',
        'margin-left': 'inherit',
    }
    assert expand_to_dict('margin: 1em') == {
        'margin-top': '1em',
        'margin-right': '1em',
        'margin-bottom': '1em',
        'margin-left': '1em',
    }
    assert expand_to_dict('padding: 1em 0') == {
        'padding-top': '1em',
        'padding-right': '0',
        'padding-bottom': '1em',
        'padding-left': '0',
    }
    assert expand_to_dict('padding: 1em 0 2em') == {
        'padding-top': '1em',
        'padding-right': '0',
        'padding-bottom': '2em',
        'padding-left': '0',
    }
    assert expand_to_dict('padding: 1em 0 2em 5px') == {
        'padding-top': '1em',
        'padding-right': '0',
        'padding-bottom': '2em',
        'padding-left': '5px',
    }
    with attest.raises(ValueError):
        list(expand_name_values('padding', PropertyValue('1 2 3 4 5')))


@suite.test
def test_expand_borders():
    assert expand_to_dict('outline: inherit') == {
        'outline-width': 'inherit',
        'outline-style': 'inherit',
        'outline-color': 'inherit',
    }
    assert expand_to_dict('outline: 2in solid invert') == {
        'outline-width': '2in',
        'outline-style': 'solid',
        'outline-color': 'invert',
    }
    assert expand_to_dict('border-top: 3px dotted red') == {
        'border-top-width': '3px',
        'border-top-style': 'dotted',
        'border-top-color': 'red',
    }
    assert expand_to_dict('border: 6px dashed green') == {
        'border-top-width': '6px',
        'border-top-style': 'dashed',
        'border-top-color': 'green',

        'border-left-width': '6px',
        'border-left-style': 'dashed',
        'border-left-color': 'green',

        'border-bottom-width': '6px',
        'border-bottom-style': 'dashed',
        'border-bottom-color': 'green',

        'border-right-width': '6px',
        'border-right-style': 'dashed',
        'border-right-color': 'green',
    }
    with attest.raises(ValueError):
        list(expand_name_values('border', PropertyValue('6px dashed left')))
