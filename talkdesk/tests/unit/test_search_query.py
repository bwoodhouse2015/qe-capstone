from app import normalize_search_query


def test_normalize_search_query_trims_collapses_and_lowercases():
    # Arrange
    raw_query = "   PYTHON    Testing   "

    # Act
    result = normalize_search_query(raw_query)

    # Assert
    assert result == "python testing"
