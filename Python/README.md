# Fogo cruzado python API

Este é um módulo em construção para acessar a API do projeto [fogo cruzadp](fogocruzado.org.br) direto do python.

Por questões de segurança, adicionem o email e a senha de acesso em u arquivo `.env` na pasta do projeto, da seguinte forma (ver [env-example](../env-example):

```
FOGO_CRUZADO_EMAIL=usuario@host.com
FOGO_CRUZADO_PASSWORD=password
```

Este projeto usa o python [poetry]() para gestão de dependencias. Para executar os testes:

```
poetry run python -m unittest
```

## Contribuindo:
Add dependencies:

```buildoutcfg
poetry add package
```
