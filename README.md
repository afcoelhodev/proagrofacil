# Desafio Softfocus - Proagro Facil

Antes de iniciar a execução da aplicação o ambiente deve ser preparado e configurado, conforme os passos abaixo:

1. Fazer o **clone** do repositorio aqui em questao 
- caso precise de orientação para realizar o clone do repositório clique neste [link](https://docs.github.com/pt/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository)

2. Após realizar o clone do repositório, acessar o **path** do diretorio no terminal ou abrir o mesmo no IDE (VSCode/Pycharm)
- no terminal **ative o ambiente virtual** e instale as dependências através do comando:
```commandline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Criar a imagem Docker atraves do docker-compose (criar o ambiente com o Python e o server do MySQL) diretamente no terminal do sistema
- caso não tenha o Docker/Docker-compose instalado na maquina, segue os links com instruções para baixar os mesmos:
    * Docker: https://docs.docker.com/install/linux/docker-ce/ubuntu/
    * Docker-compose: https://docs.docker.com/compose/install/
```commandline
docker-compose up
```

4. Após subir a imagem do docker-compose, acessar o terminal do IDE para gerar as tabelas iniciais do banco de dados através do comando:
- o path para o file é: **./proagrofacil/database/**
```commandline
python3 database.py 
```

5. Para rodar a aplicação, retorne a pasta raiz (**./proagrofacil/**) e no próprio terminal do IDE acionar pelo comando:
```commandline
python3 app.py
```

A aplicação deve rodar na porta 5000 (http://127.0.0.1:5000/ ou http://localhost:5000)

6. Com a aplicação rodando, atentar aos seguintes pontos:
    - Formatação do formulário de registro de nova comunicação de perda
        - CPF: somente numeros (sem ponto nem traço)
        - Email: no formato com @ e .br no final
        - LATITUDE/LONGITUDE: considera sinal, 8 dígitos e ponto (ex: -12.345678)
        - Data colheita: formato dd/mm/yyyy
