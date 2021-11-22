from parser import parse
import unittest
import json
from google.protobuf.json_format import MessageToDict
from data import load


class TestParser(unittest.TestCase):
    def test_jan_2020(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open("src/output_test/test_parser/expected_2020.json", "r") as fp:
            expected_2020 = json.load(fp)

        files = [
            "src/output_test/test_parser/membros-ativos-contracheque-01-2020.ods",
            "src/output_test/test_parser/membros-ativos-verbas-indenizatorias-01-2020.ods",
        ]

        dados = load(files, "2020", "01")
        result_data = parse(dados, "mpba/01/2020", 1, 2020)
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)
        self.assertEqual(expected_2020, result_to_dict)

    def test_jan_2018(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open("src/output_test/test_parser/expected_2018.json", "r") as fp:
            expected_2018 = json.load(fp)

        files = ["src/output_test/test_parser/membros-ativos-contracheque-01-2018.ods"]

        dados = load(files, "2018", "01")
        result_data = parse(dados, "mpba/01/2018", 1, 2018)
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)
        self.assertEqual(expected_2018, result_to_dict)


if __name__ == "__main__":
    unittest.main()
