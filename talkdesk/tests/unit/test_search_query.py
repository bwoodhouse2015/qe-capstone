import pytest
from fastapi import HTTPException

from app import normalize_search_query
from app import normalize_title


def test_normalize_search_query_trims_collapses_and_lowercases():
    # Arrange
    raw_query = "   PYTHON    Testing   "

    # Act
    result = normalize_search_query(raw_query)

    # Assert
    assert result == "python testing"


def test_normalize_search_query_handles_empty_string():
    # Arrange
    raw_query = ""

    # Act
    result = normalize_search_query(raw_query)

    # Assert
    assert result == ""


def test_normalize_search_query_handles_single_word():
    # Arrange
    raw_query = "Python"

    # Act
    result = normalize_search_query(raw_query)

    # Assert
    assert result == "python"


def test_normalize_title_trims_whitespace():
    # Arrange
    title = "   My Talk   "

    # Act
    result = normalize_title(title)

    # Assert
    assert result == "My Talk"


def test_normalize_title_rejects_empty_title():
    # Arrange / Act / Assert
    with pytest.raises(HTTPException) as ex:
        normalize_title("")

    assert ex.value.status_code == 400
