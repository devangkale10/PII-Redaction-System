import pytest
import spacy
import en_core_web_trf
from assignment1.censor_content import censor_content

label_mapping = {
    "NORP": "Nationalities or Religious or Political Groups",
    "GPE": "Geopolitical Entities",
    "FAC": "Facilities",
    "ORG": "Organizations",
    "PERSON": "Persons",
    "LOC": "Locations",
    "PRODUCT": "Products",
    "EVENT": "Events",
    "WORK_OF_ART": "Art Works",
    "LAW": "Laws",
    "LANGUAGE": "Languages",
    "DATE": "Dates",
    "TIME": "Times",
    "PERCENT": "Percentages",
    "MONEY": "Monetary Values",
    "QUANTITY": "Quantities",
    "ORDINAL": "Ordinal Numbers",
    "CARDINAL": "Cardinal Numbers",
    "PHONE": "Phone Numbers",
    "EMAIL": "Email IDs",
}

nlp = en_core_web_trf.load()


# The parameterized test below tests the censor_content function with different input texts and expected outputs.
# Used this to not repeat the same test multiple times.
# This will test for address, date, email, name, and phone number, one by one.
@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("IL 62701", "█" * 8),
        ("January 1, 2020", "█" * 15),
        ("contact@example.com", "█" * 19),
        ("Michael Jackson", "█" * 15),
        ("Call me at 123-456-7890", "Call me at " + "█" * 12),
    ],
)
def test_all(input_text, expected):
    censored_content, stats_output = censor_content(input_text, nlp, label_mapping)
    assert censored_content == expected
