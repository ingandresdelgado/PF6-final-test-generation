from main import dish_fetch

# Test 1
def test_trivia_fetch_returns_dict():
    result = dish_fetch(1)
    assert isinstance(result, dict)


# Test 2
def test_trivia_fetch_has_required_fields():
    result = dish_fetch(1)
    assert "id" in result
    assert "name" in result


# Test 3
def test_trivia_fetch_correct_id():
    result = dish_fetch(5)
    assert result["id"] == 5

# Test 4
def test_trivia_fetch_name_not_empty():
    result = dish_fetch(1)
    assert result["name"]
    assert isinstance(result["name"], str)

# Test 5
def test_trivia_fetch_accepts_numbers():
    result = dish_fetch(15)
    assert result is not None
