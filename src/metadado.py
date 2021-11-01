from coleta import coleta_pb2 as Coleta


def captura(mes, ano):
    metadado = Coleta.Metadados()
    metadado.nao_requer_login = True
    metadado.nao_requer_captcha = True
    metadado.acesso = Coleta.Metadados.FormaDeAcesso.AMIGAVEL_PARA_RASPAGEM
    metadado.extensao = Coleta.Metadados.Extensao.ODS
    metadado.estritamente_tabular = False
    if ano == 2019 and mes == 7:
        metadado.formato_consistente = False
    else:
        metadado.formato_consistente = True
    metadado.tem_matricula = True
    metadado.tem_lotacao = True
    metadado.tem_cargo = True
    metadado.receita_base = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
    metadado.despesas = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
    metadado.outras_receitas = Coleta.Metadados.OpcoesDetalhamento.DETALHADO

    return metadado
