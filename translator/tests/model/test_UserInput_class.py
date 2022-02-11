import ltrans
import pytest


def test_create_object():
    user_input = ltrans.model.UserInput(r'Good\n morning', 'English',
                                        'Spanish', True, False)
    assert user_input.text_lines == r'Good\n morning'
    assert user_input.src_language == 'English'
    assert user_input.destination_language == 'Spanish'
    assert user_input.is_add_src is True
    assert user_input.is_add_transliteration is False


def test_property_attribute():
    user_input = ltrans.model.UserInput(r'Hello', 'English',
                                        'Spanish', True, False)
    with pytest.raises(AttributeError):
        user_input.text_lines = 'Hi'
