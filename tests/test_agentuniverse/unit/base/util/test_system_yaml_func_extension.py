# !/usr/bin/env python3
# -*- coding:utf-8 -*-

import unittest

from agentuniverse.base.util.system_util import process_dict_with_funcs, process_yaml_func


class YamlFuncWithoutExtensionTest(unittest.TestCase):
    """An @FUNC expression cannot be resolved without a yaml_func_extension instance.

    Historically both processors silently returned the literal expression as the
    value, so a misconfigured api_key surfaced as a cryptic upstream 401 instead
    of the documented ValueError (issue #3814).
    """

    def test_func_expression_without_extension_raises(self):
        with self.assertRaises(ValueError) as ctx:
            process_yaml_func('@FUNC(load_api_key("qwen"))', None)
        self.assertIn("yaml_func_extension.py is required", str(ctx.exception))

    def test_plain_value_without_extension_passes_through(self):
        self.assertEqual(process_yaml_func("sk-plain", None), "sk-plain")
        self.assertIsNone(process_yaml_func(None, None))

    def test_dict_with_func_expression_without_extension_raises(self):
        profile = {"name": "qwen", "api_key": '@FUNC(load_api_key("qwen"))'}
        with self.assertRaises(ValueError) as ctx:
            process_dict_with_funcs(profile, None)
        self.assertIn("yaml_func_extension.py is required", str(ctx.exception))

    def test_dict_without_func_expressions_passes_through(self):
        profile = {"name": "qwen", "api_key": "sk-plain", "nested": {"model": "qwen-max"}}
        self.assertEqual(process_dict_with_funcs(profile, None), profile)

    def test_nested_dict_func_expression_without_extension_raises(self):
        profile = {"llm_model": {"name": "qwen", "api_key": '@FUNC(load_key())'}}
        with self.assertRaises(ValueError):
            process_dict_with_funcs(profile, None)


if __name__ == "__main__":
    unittest.main()
