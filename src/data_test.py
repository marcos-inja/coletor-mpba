from data import load
import unittest

file_names = [
    "src/output_test/test_parser/Membros ativos-contracheque-01-2020.ods",
    "src/output_test/test_parser/Membros ativos-Verbas Indenizatorias-01-2020.ods",
]


class TestData(unittest.TestCase):
    def test_validate_rows(self):
        STATUS_INVALID_FILE = 5
        with self.assertRaises(SystemExit) as cm:
            dados = load(file_names, "2020", "01")
            dados.validate()
        self.assertEqual(cm.exception.code, STATUS_INVALID_FILE)

    def test_validate_existence(self):
        STATUS_DATA_UNAVAILABLE = 4
        with self.assertRaises(SystemExit) as cm:
            dados = load(file_names, "2021", "01")
            dados.validate()
        self.assertEqual(cm.exception.code, STATUS_DATA_UNAVAILABLE)


if __name__ == "__main__":
    unittest.main()
