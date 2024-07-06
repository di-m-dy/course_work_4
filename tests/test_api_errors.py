import os
import sys


from src.api_errors import (
    ApiBaseError,
    ApiQueryError,
    AttrIntersectionError,
    AttrValueRestrictionError
)


def test_api_base_error():
    error = ApiBaseError()
    assert str(error) == "Base error"
    error = ApiBaseError("Test")
    assert str(error) == "Test"


def test_api_query_error():
    error = ApiQueryError()
    assert str(error) == "Query error"
    error = ApiQueryError("Test")
    assert str(error) == "Test"


def test_attr_intersection_error():
    error = AttrIntersectionError()
    assert str(error) == "Attributes intersect"
    error = AttrIntersectionError("Test")
    assert str(error) == "Test"


def test_attr_value_restriction_error():
    error = AttrValueRestrictionError()
    assert str(error) == "Restriction value"
    error = AttrValueRestrictionError("Test")
    assert str(error) == "Test"
