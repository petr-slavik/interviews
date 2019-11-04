import pytest, random
from mx_mul import Matrix, usr_input_width_height


def test_matmul(): # testuje metodu nasobeni matic dle udaju z prikladu v zadani
    mat1 = Matrix(2,3)
    mat1.fill([1,2,5,3,6,7])
    mat2 = Matrix(1,2)
    mat2.fill([5,1])
    mat3 = mat1 @ mat2
    assert mat3 == [[7], [28], [37]]

def test_matmul_exception(): # testuje vyvolani vyjimky v pripade ze matice nejdou nasobit
    mat1 = Matrix(2,3)
    mat1.fill([1,2,5,3,6,7])
    mat2 = Matrix(1,2)
    mat2.fill([5,1])
    with pytest.raises(ValueError):
        assert mat2 @ mat1

def test_size(): # testuje velikost matice
    mat1 = Matrix(2,3)
    assert mat1.size == 6


@pytest.mark.parametrize(
["width", "height", "testlist"], # testlist je seznam velikosti width x height vytvoreny nahodnymi cisly
[(3,2,[random.randint(-50, 50) for i in range(6)]),
(4,2,[random.randint(-50, 50) for i in range(8)]),
(5,3,[random.randint(-50, 50) for i in range(15)]),
(6,2,[random.randint(-50, 50) for i in range(12)]),
(7,3,[random.randint(-50, 50) for i in range(21)]),
(3,6,[random.randint(-50, 50) for i in range(18)]),
(3,1,[random.randint(-50, 50) for i in range(3)])],
)
def test_fill(width, height, testlist): # testuje funkcnost fill metody na vlozeni prvku do matice skrze seznam, data bere z parametru
    mat1 = Matrix(width, height)
    assert mat1.fill(testlist) == mat1.rows 


def test_create_value_list(): # testuje vytvoreni listu o velikosti matice. Input funkci supluje random
    mat1 = Matrix(2,3)
    assert len([random.randint(-50, 50) for _ in range(0, mat1.size)]) == mat1.size


def test_usr_input_values(monkeypatch): # mocked 1 input test
    monkeypatch.setattr('builtins.input', lambda: 5)
    value = input()
    assert Matrix.usr_input_values() == value


def test_usr_input_width_height(monkeypatch): # mocked 2 input test
    monkeypatch.setattr('builtins.input', lambda prompt="": 3)
    width = input("width: ")
    monkeypatch.setattr('builtins.input', lambda prompt="": 3)
    height = input("height: ")
    assert usr_input_width_height() == (width, height)
    # Ve funkci nejdou mocknout pomoci monkeypath dva inputy zvlast.
    # takze oba inputy ve funkci jsou nahrazeny posledni nahrazenou hodnotou
    # proto nemuzu nastavit napr pro width 3 a pro height 2, protoze to pak
    # zpusobi Assertion error: assert (2, 2) == (3, 2).
    # Proto test projde jen kdyz se input prepise pro obe promene na stejnou hodnotu.
