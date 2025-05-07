import pytest
from apps.orders.domain.value_objects import Money


def test_money_equality():
    assert Money(100) == Money(100)
    assert not (Money(100) == Money(50))

@pytest.mark.parametrize("a,b,expected", [(50,50,100), (0,0,0), (30,20,50)])
def test_money_add(a, b, expected):
    result = Money(a) + Money(b)
    assert isinstance(result, Money)
    assert result.amount == expected


def test_money_negative_raises():
    with pytest.raises(ValueError):
        Money(-10)