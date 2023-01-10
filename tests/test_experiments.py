import unittest
from unittest.mock import patch

from tests import case


def main():
    result_1 = read_file('racers')
    result_2 = read_file('start_time')
    result_3 = read_file('end_time')
    # Далее идут ваши действия с этими результатами

def read_file(filename):
    # Код чтения файла
    return case

class TestMain(unittest.TestCase):
    @patch('__main__.read_file')
    def test_main(self, mock_read_file):
        # Прописываем значения, которые будет возвращать функция read_file
        mock_read_file.side_effect = ['racers_result', 'start_time_result', 'end_time_result']

        main()

        # Проверяем, что функция read_file была вызвана 3 раза с правильными аргументами
        mock_read_file.assert_any_call('racers')
        mock_read_file.assert_any_call('start_time')
        mock_read_file.assert_any_call('end_time')


if __name__ == '__main__':
    unittest.main()
