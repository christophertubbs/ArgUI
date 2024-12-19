"""
Unit tests for `argui.utilities.common`
"""
import typing
import unittest
import types

from argui.utilities import common

EPSILON: float = 0.0001


class TestGetElementByName(unittest.TestCase):
    """Tests for `argui.utilities.common.get_element_by_name`"""
    def test_globals(self):
        """
        Tests to ensure that elements can be found by name from the available global context
        """
        context: typing.Dict[str, typing.Any] = globals()

        self.assertEqual(common.get_element_by_name("unittest.util", context), unittest.util)
        self.assertEqual(common.get_element_by_name("unittest.TestCase", context), unittest.TestCase)
        self.assertEqual(common.get_element_by_name("unittest.signals.wraps", context), unittest.signals.wraps)
        self.assertEqual(common.get_element_by_name("typing", context), typing)
        self.assertEqual(common.get_element_by_name("typing.Mapping", context), typing.Mapping)

        with self.assertRaises(KeyError):
            common.get_element_by_name("JeremyBerimy", context)

    def test_manual_context(self):
        """
        Tests to ensure that elements can be found by name within a manually provided dictionary
        """
        context: typing.Dict[str, typing.Any] = {
            "one": True,
            "two": {3, 4, 5},
            "three": [
                6,
                7,
                8
            ],
            "four": {
                "a": "A",
                "b": "B",
                "c": "C",
            },
            "five": typing.Mapping,
            "eps": EPSILON,
            "ut": unittest
        }
        
        for key, value in context.items():
            self.assertEqual(common.get_element_by_name(key, context), value)

            if isinstance(value, types.ModuleType):
                module_members: typing.Iterable[str] = dir(value)

                for member in module_members:
                    full_key = f"{key}.{member}"
                    self.assertEqual(
                        common.get_element_by_name(full_key, context),
                        getattr(value, member)
                    )
            elif isinstance(value, typing.Mapping):
                for inner_key, inner_value in value.items():
                    full_key = f"{key}.{inner_key}"
                    self.assertEqual(common.get_element_by_name(full_key, context), inner_value)

        with self.assertRaises(KeyError):
            common.get_element_by_name("JeremyBerimy", context)

        with self.assertRaises(TypeError):
            common.get_element_by_name("four.a.__add__", context)

    def test_module(self):
        """
        Tests to ensure that elements can be found within passed modules
        """
        context: types.ModuleType = unittest

        self.assertEqual(common.get_element_by_name("util", context), unittest.util)
        self.assertEqual(common.get_element_by_name("TestCase", context), unittest.TestCase)
        self.assertEqual(
            common.get_element_by_name("signals.wraps", context),
            unittest.signals.wraps
        )

        with self.assertRaises(KeyError):
            common.get_element_by_name("JeremyBerimy", context)


    def test_locals(self):
        """
        Tests to ensure that elements may be found from within the local context
        """
        # Add variables
        number_1: int = 5
        number_2: float = 23.2342342342
        collection_one: typing.List[int] = [1, 2, 3, 4, 5]
        collection_two: typing.Set[str] = {"one", "two", "three"}
        mapping: typing.Mapping[str, int] = {
            "one": 1,
            "two": 2,
            "three": 3
        }
        boolean: bool = False
        sigs: types.ModuleType = unittest.signals

        context: typing.Dict[str, typing.Any] = locals()

        self.assertEqual(common.get_element_by_name("number_1", context), number_1)
        self.assertAlmostEqual(common.get_element_by_name("number_2", context=context), number_2, delta=EPSILON)
        self.assertEqual(common.get_element_by_name("collection_one", context), collection_one)
        self.assertEqual(common.get_element_by_name("collection_two", context), collection_two)
        self.assertDictEqual(common.get_element_by_name("mapping", context), mapping)
        self.assertEqual(common.get_element_by_name("boolean", context), boolean)

        self.assertEqual(common.get_element_by_name("sigs.wraps", context), unittest.signals.wraps)
        self.assertEqual(common.get_element_by_name("mapping.one", context), mapping["one"])

        with self.assertRaises(KeyError):
            common.get_element_by_name("JeremyBerimy", context)
