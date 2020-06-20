from json import JSONEncoder
from typing import Any

import pytest

from nichtparasoup.webserver import _SimpleJsonEncoder


class TestSimpleJsonEncoder:

    @pytest.mark.parametrize(
        'data',
        [
            None,
            False, True,
            1, -0.2, 'foo',
            [1, 2], (1, 2),
            {'a': 1, 2: 3},
        ],
        ids=type
    )
    def test_base_type(self, data: Any) -> None:
        # act
        json_o = JSONEncoder().encode(data)
        json_c = _SimpleJsonEncoder().encode(data)
        # assert
        assert json_o == json_c

    @pytest.mark.parametrize(
        'data_o',
        [
            1, -0.2, 'foo',
            [1, 2], (1, 2),
            {'a': 1, 2: 3},
        ],
        ids=type
    )
    def test_inherited_base_type(self, data_o: Any) -> None:
        # arrange
        type_o = type(data_o)

        class Inherited(type_o):  # type: ignore[valid-type,misc]
            pass

        data_i = Inherited(data_o)
        # act
        json_o = JSONEncoder().encode(data_o)
        json_i = _SimpleJsonEncoder().encode(data_i)
        # assert
        assert json_o == json_i

    def test_custom_object(self) -> None:
        # arrange
        class Foo:
            def __init__(self, a: Any, b: Any, *args: Any, **kwargs: Any) -> None:
                self.a = a
                self.b = b
                self.args = args
                self.kwargs = kwargs

        data_o = {
            'a': 1,
            'b': False,
            'args': ['bar'],
            'kwargs': {
                'again': {
                    'a': 0.2,
                    'b': None,
                    'args': [[True], {'a': -1}],
                    'kwargs': {
                        'tuple': (3, 2, 1)
                    },
                },
            },
        }
        data_i = Foo(1, False, 'bar', again=Foo(0.2, None, [True], {'a': -1}, tuple=(3, 2, 1)))
        # act
        json_o = JSONEncoder().encode(data_o)
        json_i = _SimpleJsonEncoder().encode(data_i)
        # assert
        assert json_o == json_i
