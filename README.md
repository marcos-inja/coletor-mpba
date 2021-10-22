# Ministério Público do Estado da Bahia (MP-BA)

Este crawler tem como objetivo a recuperação de informações sobre folhas de pagamentos
dos funcionários do Ministério Público do Estado da Bahia (MP-BA). O site com as informações
pode ser acessado [aqui](https://lai.sistemas.mpba.mp.br/).

O crawler está estruturado como uma CLI. Você passa dois argumentos (mês e ano) e é impresso um
**JSON** representando a folha de pagamento da instituição.

## Legislação

Os dados devem estar de acordo com a [Resolução 102 do CNJ](https://atos.cnj.jus.br/atos/detalhar/69).

## Arquivos
  
### Remunerações

O acesso pode ser feito a partir de uma API:

- **URL Base**: [https://lai-app.sistemas.mpba.mp.br/api/quadroremuneratoriogeral/consultar?mes={mes}&ano={ano}&cargo=0](https://lai-app.sistemas.mpba.mp.br/api/quadroremuneratoriogeral/consultar?mes=10&ano=2020&cargo=0)
- **Formato**: JSON