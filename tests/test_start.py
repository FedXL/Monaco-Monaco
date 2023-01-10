import sys
from unittest.mock import patch, Mock, MagicMock


from start import main

from unittest.mock import MagicMock


def test_function(arg1, arg2):
    # Call to the function you want to mock
    result = my_function(arg1, arg2)
    print(result)


def my_function(arg1, arg2):
    return arg1 + arg2


my_function = MagicMock(side_effect=[5, 10, 15])

test_function(1, 2)  # prints 5
test_function(2, 2)  # prints 10
test_function(3, 2)  # prints 15

@patch('sys.argv', ['start.py', '--files', 'C:\\Users\\Asus\\PycharmProjects\\monaco\\storage', '--driver', 'Sergey Sirotkin'])
def test_main(capsys):
    """Тест файл не найден 2 аргумента"""
    main()
    captured = capsys.readouterr()
    assert captured.out.split("\n") == ['DNF | Sergey Sirotkin WILLIAMS MERCEDES | INVALID TIME',
 '_________________________________________________________________',
 '']


def test_mock_power():
    mock = Mock()
    read_file = mock


# @patch('sys.argv', ['collection_framework.py', '--file', 'uniq\\file.png', '--string', 'fwfowifjw'])
# @patch(brains.build_data.)
# def test_main_broken_text(open_mock,capsys):
#     """Негативный тест """
#     open_mock.return_value = b'\x03\x00\x15\x07\nY\x1c\n\x0b\x07\x01'
#     main()
#     captured = capsys.readouterr()
#     assert captured.out == "Sorry we have an unexpected error." + "\n"

