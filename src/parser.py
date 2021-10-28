# coding: utf8
import pandas as pd
import sys
import os
from coleta import coleta_pb2 as Coleta

CONTRACHEQUE_ATE_JUNHO_2019 = "contracheque"
CONTRACHEQUE_DEPOIS_JUNHO_2019 = "contracheque"
INDENIZACOES = "indenizações"

HEADERS = {
    CONTRACHEQUE_ATE_JUNHO_2019: {
        "Remuneração do Cargo Efetivo": 4,
        "Outras Verbas Remuneratórias, Legais ou Judiciais": 5,
        "Função de Confiança ou Cargo em Comissão": 6,
        "Gratificação Natalina": 7,
        "Férias (1/3 constitucional)": 8,
        "Abono de Permanência": 9,
        "Contribuição Previdenciária": 11,
        "Imposto de Renda": 12,
        "Retenção por Teto Constitucional": 13,
        "Indenizações": 16,
        "Outras Remunerações Retroativas / Temporárias": 17,
    },
    CONTRACHEQUE_DEPOIS_JUNHO_2019: {
        "Remuneração do Cargo Efetivo": 4,
        "Outras Verbas Remuneratórias, Legais ou Judiciais": 5,
        "Função de Confiança ou Cargo em Comissão": 6,
        "Gratificação Natalina": 7,
        "Férias (1/3 constitucional)": 8,
        "Abono de Permanência": 9,
        "Outras Remunerações Temporárias": 10,
        "Verbas indenizatórias": 11,
        "Contribuição Previdenciária": 13,
        "Imposto de Renda": 14,
        "Retenção por Teto Constitucional": 15,
    },
    INDENIZACOES: {
        "Auxílio-alimentação": 4,
        "Auxílio-transporte": 5,
        "Auxílio Moradia": 6,
        "Auxílio Natalidade": 7,
        "Substituição Membros": 8,
        "Ajuda de Custo": 9,
        "Serviço Extraordinário": 10,
        "Substituição de Função": 11,
        "Gratificação de Serviços Especiais": 12,
        "Diferença de Entrância": 13,
    },
}


def parse_employees(fn, chave_coleta, mes, ano):
    employees = {}
    counter = 1
    for row in fn:
        name = row[1]
        if not isNaN(name) and name != "0" and name != "Nome":
            membro = Coleta.ContraCheque()
            membro.id_contra_cheque = chave_coleta + "/" + str(counter)
            membro.chave_coleta = chave_coleta
            membro.nome = name
            membro.tipo = Coleta.ContraCheque.Tipo.Value("MEMBRO")
            membro.ativo = True
            if int(ano) == 2018 or (int(ano) == 2019 and int(mes) < 7):
                membro.remuneracoes.CopyFrom(
                    cria_remuneracao(row, CONTRACHEQUE_ATE_JUNHO_2019)
                )
            else:
                membro.remuneracoes.CopyFrom(
                    cria_remuneracao(row, CONTRACHEQUE_DEPOIS_JUNHO_2019)
                )
            employees[name] = membro
            counter += 1
    return employees


def cria_remuneracao(row, categoria):
    remu_array = Coleta.Remuneracoes()
    items = list(HEADERS[categoria].items())
    for i in range(len(items)):
        key, value = items[i][0], items[i][1]
        remuneracao = Coleta.Remuneracao()
        remuneracao.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneracao.categoria = categoria
        remuneracao.item = key
        remuneracao.valor = float(format_value(row[value]))
        remuneracao.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
        if (
            categoria == CONTRACHEQUE_ATE_JUNHO_2019
            or categoria == CONTRACHEQUE_DEPOIS_JUNHO_2019
        ) and value in [4, 5]:
            remuneracao.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("B")
        if categoria == CONTRACHEQUE_ATE_JUNHO_2019 and value in [11, 12, 13]:
            remuneracao.valor = remuneracao.valor * (-1)
            remuneracao.natureza = Coleta.Remuneracao.Natureza.Value("D")
        if categoria == CONTRACHEQUE_DEPOIS_JUNHO_2019 and value in [13, 14, 15]:
            remuneracao.valor = remuneracao.valor * (-1)
            remuneracao.natureza = Coleta.Remuneracao.Natureza.Value("D")

        remu_array.remuneracao.append(remuneracao)
    return remu_array


def update_employees(fn, employees, categoria):
    for row in fn:
        name = row[1]
        if name in employees.keys():
            emp = employees[name]
            remu = cria_remuneracao(row, categoria)
            emp.remuneracoes.MergeFrom(remu)
            employees[name] = emp
    return employees


def isNaN(string):
    return string != string


def parse(data, chave_coleta, mes, ano):
    employees = {}
    folha = Coleta.FolhaDePagamento()
    try:
        employees.update(parse_employees(data.contracheque, chave_coleta, mes, ano))
        update_employees(data.indenizatorias, employees, INDENIZACOES)

    except KeyError as e:
        sys.stderr.write(
            "Registro inválido ao processar verbas indenizatórias: {}".format(e)
        )
        os._exit(1)
    for i in employees.values():
        folha.contra_cheque.append(i)
    return folha
    # return list(employees.values())


def format_value(element):
    # A value was found with incorrect formatting. (3,045.99 instead of 3045.99)
    if isNaN(element):
        return 0.0
    if type(element) == str:
        if "." in element and "," in element:
            element = element.replace(".", "").replace(",", ".")
        elif "," in element:
            element = element.replace(",", ".")
        elif "-" in element:
            element = 0.0

    return float(element)
