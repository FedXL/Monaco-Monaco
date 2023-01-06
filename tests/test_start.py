from unittest.mock import patch

from start import main


@patch('sys.argv', ['start.py', '--files', 'C:\\Users\\Asus\\PycharmProjects\\monaco\\storage', '--desc'])
def test_main(capsys):
    """Тест файл не найден 2 аргумента"""
    main()
    captured = capsys.readouterr()
    print(captured)
    assert captured == "f"



# @patch('sys.argv', ['collection_framework.py', '--file', 'uniq\\file.png', '--string', 'fwfowifjw'])
# @patch(brains.build_data.)
# def test_main_broken_text(open_mock,capsys):
#     """Негативный тест """
#     open_mock.return_value = b'\x03\x00\x15\x07\nY\x1c\n\x0b\x07\x01'
#     main()
#     captured = capsys.readouterr()
#     assert captured.out == "Sorry we have an unexpected error." + "\n"

