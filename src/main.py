# coding: utf8
import sys
import os
import crawler
#from parser import parse
from coleta import coleta_pb2 as Coleta, IDColeta
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf import text_format

if "YEAR" in os.environ:
    year = os.environ["YEAR"]
else:
    sys.stderr.write("Invalid arguments, missing parameter: 'YEAR'.\n")
    os._exit(1)

if "MONTH" in os.environ:
    month = os.environ["MONTH"]
    month = month.zfill(2)
else:
    sys.stderr.write("Invalid arguments, missing parameter: 'MONTH'.\n")
    os._exit(1)

if "OUTPUT_FOLDER" in os.environ:
    output_path = os.environ["OUTPUT_FOLDER"]
else:
    output_path = "./output"

if "GIT_COMMIT" in os.environ:
    crawler_version = os.environ["GIT_COMMIT"]
else:
    crawler_version = "unspecified"

# Main execution
def main():
    file_names = crawler.crawl(year, month, output_path)

    # Cria objeto com dados da coleta.
    coleta = Coleta.Coleta()
    coleta.orgao = "mpba"
    coleta.mes = int(month)
    coleta.ano = int(year)
    coleta.repositorio_coletor = "https://github.com/dadosjusbr/coletor-mpba"
    coleta.versao_coletor = crawler_version
    coleta.arquivos.extend(file_names)
    timestamp = Timestamp()
    timestamp.GetCurrentTime()
    coleta.timestamp_coleta.CopyFrom(timestamp)


if __name__ == "__main__":
    main()
