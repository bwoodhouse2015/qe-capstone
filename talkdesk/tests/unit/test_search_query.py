import pytest
from fastapi import HTTPException

from app import normalize_search_query  ##calls function from app.py
from app import normalize_title


def test_normalize_search_query_trims_collapses_and_lowercases():

    raw_query = "   PYTHON    Testing   "  ##Data that is input for the test


    result = normalize_search_query(raw_query)  ##This is the returned value


    assert result == "python testing" ##This verifies the output

    ##"if I give this function a value, does it return the expected result?"
    ## What the test is actually doing: Removes extra spaces, converts text to lowercase and returns that expected value


def test_normalize_search_query_handles_empty_string():

    raw_query = "" ##Data input


    result = normalize_search_query(raw_query) ##Returned value


    assert result == "" ##Expected result

    ## This test is for empty searches


def test_normalize_search_query_handles_single_word():

    raw_query = "Python"


    result = normalize_search_query(raw_query)


    assert result == "python"


def test_normalize_title_trims_whitespace():

    title = "   My Talk   " ##Data input, has spaces, test is specifically for titles


    result = normalize_title(title) ##Returned value.


    assert result == "My Talk" ##Expected result, verifies that the white space cleans up.


def test_normalize_title_rejects_empty_title():

    with pytest.raises(HTTPException) as ex:
        normalize_title("")

    assert ex.value.status_code == 400 ##expected result
##This test is similar to the empty string search unit test, but with this result, it expects an error 400 and if it doesn't get that expected returned value the test with fail. Where at the other test is just verifying that there is space there while trying to input data
