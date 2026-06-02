#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
variable_parser.py — Runtime prompt variable substitution utility.

Usage:
    from utils.variable_parser import parse_prompt

    result = parse_prompt(
        "Summarize {{Document_Title}} for {{Audience}}.",
        {"Document_Title": "Q1 Review Deck", "Audience": "the executive team"}
    )
    # -> "Summarize Q1 Review Deck for the executive team."
"""

import re


def parse_prompt(prompt_str: str, variables: dict) -> str:
    """
    Replace all {{KEY}} placeholders in prompt_str with values from variables.

    Args:
        prompt_str: The prompt template string containing {{KEY}} placeholders.
        variables:  Dict mapping placeholder keys to replacement values.

    Returns:
        The prompt string with all placeholders replaced.

    Raises:
        KeyError: If a placeholder key is present in the prompt but not in variables.
        TypeError: If prompt_str is not a string or variables is not a dict.
    """
    if not isinstance(prompt_str, str):
        raise TypeError(f"prompt_str must be a string, got {type(prompt_str).__name__}")
    if not isinstance(variables, dict):
        raise TypeError(f"variables must be a dict, got {type(variables).__name__}")

    def replace_match(match: re.Match) -> str:
        key = match.group(1)
        if key not in variables:
            raise KeyError(f"'{key}' not found in variables dict — add it before calling parse_prompt()")
        return str(variables[key])

    return re.sub(r"\{\{(\w+)\}\}", replace_match, prompt_str)


def list_variables(prompt_str: str) -> list[str]:
    """
    Return a list of all unique {{KEY}} placeholder names found in prompt_str.
    Useful for validating that a variables dict is complete before substitution.
    """
    return list(dict.fromkeys(re.findall(r"\{\{(\w+)\}\}", prompt_str)))


# ---------------------------------------------------------------------------
# Quick self-test (run directly: python utils/variable_parser.py)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    test_prompt = "Hello {{Name}}, please summarize {{Document_Title}}."
    test_vars = {"Name": "World", "Document_Title": "Q1 Review"}

    result = parse_prompt(test_prompt, test_vars)
    expected = "Hello World, please summarize Q1 Review."
    assert result == expected, f"FAIL: got {result!r}"
    print(f"PASS: {result!r}")

    # Test missing key raises KeyError
    try:
        parse_prompt("Hello {{Missing}}", {})
        print("FAIL: expected KeyError not raised")
    except KeyError as e:
        print(f"PASS: KeyError raised for missing key: {e}")

    # Test list_variables
    keys = list_variables(test_prompt)
    assert keys == ["Name", "Document_Title"], f"FAIL: {keys}"
    print(f"PASS: list_variables -> {keys}")
