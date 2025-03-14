# Projeto final Docker - Guia de Implementação

Este projeto implementa um ambiente completo de monitoramento de dados usando
Metabase, PostgreSQL e um gerador de dados simulados, tudo containerizado e
orquestrado com Docker Compose.

## Sumário <!--toc:start-->

- [Pré-requisitos](#pré-requisitos)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Configuração](#configuração)
- [Execução](#execução)
- [Autor](#autor) <!--toc:end-->

## Pré-requisitos

- Docker (versão 20.10.0 ou superior)
- Docker Compose (versão 2.0.0 ou superior)
- Git

## Estrutura do Projeto

``` ├── docker-compose.yml ├── .env ├── README.md ├── data-generator/ │   ├──
Dockerfile │   ├── requirements.txt │   └── app/ │       └── generate_data.py
├── nginx/ │   ├── Dockerfile │   └── nginx.conf └── postgres/ └── init.sql ```

## Guia de Implementação

Nesse projeto, você precisar orquestrar 4 containers responsáveis pelo
funcionamento de uma aplicação. Teremos:

- 2 Containers do **postgreSQL**
- 1 Container do **Metabase**
- 1 Container do **Nginx**

> Para entender o propósito de cada ferramente, refira-se ao [Guia de
> ferramentas](./Guia-ferramentas.md).

No projeto existem diversos campos faltantes no `docker-compose.yml` e no
`Dockerfile` de cada módulo, você precisará preencher esses campos e permitir
que os containers interajam perfeitamente entre si e que a memória da aplicação
seja persistente, pois você não quer perder os dados da sua aplicação não é
mesmo?

> [!NOTE] Todos os containers precisaram estar conectados entre si via uma rede
> interna.

## Configuração

1. Clone este repositório:

  ```bash git clone
  https://github.com/PETCC-UFRN/docker-2025.1-final-project.git cd
  docker-2025.1-final-project

2. Edite o arquivo `.env` conforme necessário.

## Execução

1. Inicie todos os serviços:

  ```bash docker compose up -d ```

2. Verifique se todos os containers estão rodando:

```bash docker compose ps ```

## Autor

Vinicius de Lima, PETCC &copy; 2025
