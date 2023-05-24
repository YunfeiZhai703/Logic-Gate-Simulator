import pytest
from names import Names


@pytest.fixture
def new_names():
    names = Names()
    names.names = ["G1", "G2"]
    return names


def test_unique_error_codes(new_names):
    num_error_codes = 10
    codes = new_names.unique_error_codes(num_error_codes)

    assert new_names.error_code_count == num_error_codes
    assert codes == range(0, num_error_codes)


def test_unique_error_errors(new_names):
    with pytest.raises(TypeError):
        new_names.unique_error_codes(0.1)
    with pytest.raises(TypeError):
        new_names.unique_error_codes("test")


def test_query(new_names):
    """Test if query returns correct name ID for name_string."""
    print(new_names.names)
    assert new_names.query("G2") == 1
    assert new_names.query("G1") == 0
    assert new_names.query('test') is None


def test_lookup(new_names):
    assert new_names.lookup(["G1", "G2"]) == [0, 1]
    assert new_names.lookup(["G3", "G4"]) == [2, 3]
    assert new_names.lookup(["G4", "G1"]) == [3, 0]
    assert new_names.lookup(["G5", "G3"]) == [4, 2]


def test_lookup_adds_names(new_names):
    assert new_names.query("G3") is None
    assert new_names.lookup(["G3"]) == [2]
    assert new_names.query("G3") == 2


def test_lookup_errors(new_names):
    invalid_name_string = ["test", 0.1, new_names, (5, 5)]
    with pytest.raises(TypeError):
        new_names.lookup(invalid_name_string)


def test_get_name_string(new_names):
    assert new_names.get_name_string(0) == "G1"
    assert new_names.get_name_string(1) == "G2"
    assert new_names.get_name_string(20) is None


def test_get_name_string_gives_errors(new_names):
    with pytest.raises(TypeError):
        new_names.get_name_string("test")
    with pytest.raises(ValueError):
        new_names.get_name_string(-1)
