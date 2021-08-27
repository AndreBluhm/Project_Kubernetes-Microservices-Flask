from app import change

# Test with: "pytest"

def test_change():
    assert [{5: 'quarters'}, {1: 'nickels'}, {4: 'pennies'}] == change(1.34)