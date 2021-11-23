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

Os dados liberados pelo MPBA até Julho de 2019 estão todos no arquivo Membros ativos-contracheque, a partir desse mês é liberado também o arquivo Membros ativos-Verbas Indenizatorias, causando assim uma modificação nas colunas do arquivo contracheque (que foi avaliado também na hora de escrever seus metadados).

## Como usar

### Executando com Docker

- Inicialmente é preciso instalar o [Docker](https://docs.docker.com/install/). 

- Construção da imagem:

    ```sh
    $ cd coletor-mpba
    $ sudo docker build -t mpba .
    ```
- Execução:

    ```sh
    $ sudo docker run -e YEAR=2018 -e MONTH=1 -e GIT_COMMIT=$(git rev-list -1 HEAD) mpba
    ```

### Execução sem Docker:

- Para executar o script é necessário rodar o seguinte comando, a partir do diretório coletor-mpba, adicionando às variáveis seus respectivos valores, a depender da consulta desejada. É válido lembrar que faz-se necessario ter o [Python 3.6.9](https://www.python.org/downloads/) instalado.
 
    ```sh
        YEAR=2018 MONTH=01 GIT_COMMIT=$(git rev-list -1 HEAD) python3 src/main.py
    ```
- Para que a execução do script possa ser corretamente executada é necessário que todos os requirements sejam devidamente instalados. Para isso, executar o [PIP](https://pip.pypa.io/en/stable/installing/) passando o arquivo requiments.txt, por meio do seguinte comando:
   
    ```sh
        pip install -r requirements.txt
    ```