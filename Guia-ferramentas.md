# Guia sobre Nginx, Metabase e PostgreSQL para o Projeto Final

Este guia oferece uma visão geral das principais tecnologias usadas no projeto final do curso de Docker, explicando o que são e como interagem para criar um sistema de dashboard de monitoramento de dados.

## Sumário

<!--toc:start-->
- [PostgreSQL: O Banco de Dados](#postgresql-o-banco-de-dados)
  - [O que é PostgreSQL?](#o-que-é-postgresql)
  - [Principais características](#principais-características)
  - [Como o PostgreSQL se encaixa no projeto](#como-o-postgresql-se-encaixa-no-projeto)
- [Metabase: A Ferramenta de Visualização](#metabase-a-ferramenta-de-visualização)
  - [O que é Metabase?](#o-que-é-metabase)
  - [Principais características](#principais-características)
  - [Como o Metabase se encaixa no projeto](#como-o-metabase-se-encaixa-no-projeto)
- [Nginx: O Servidor Web e Proxy Reverso](#nginx-o-servidor-web-e-proxy-reverso)
  - [O que é Nginx?](#o-que-é-nginx)
  - [Principais características](#principais-características)
  - [Como o Nginx se encaixa no projeto](#como-o-nginx-se-encaixa-no-projeto)
- [Como Estas Tecnologias Trabalham Juntas](#como-estas-tecnologias-trabalham-juntas)
- [Containerização com Docker](#containerização-com-docker)
- [Autor](#autor)
<!--toc:end-->

## PostgreSQL: O Banco de Dados

### O que é PostgreSQL?

PostgreSQL (ou simplesmente "Postgres") é um sistema de gerenciamento de banco de dados relacional (RDBMS) de código aberto e extremamente poderoso. Criado há mais de 30 anos, o PostgreSQL é reconhecido por sua confiabilidade, robustez e conformidade com padrões SQL.

### Principais características

- **Relacional**: Organiza dados em tabelas com relações claramente definidas entre elas
- **Extensível**: Permite criar tipos de dados personalizados, funções e até linguagens de procedimento

### Como o PostgreSQL se encaixa no projeto

No nosso projeto de dashboard, o PostgreSQL desempenha duas funções essenciais:

1. **Armazenamento de dados simulados**: O serviço gerador de dados em Python armazena informações de vendas e tráfego web no PostgreSQL, criando um conjunto de dados que pode ser analisado
2. **Metadados do Metabase**: O próprio Metabase usa o PostgreSQL para armazenar suas configurações, consultas salvas, dashboards e outras informações de sistema

O PostgreSQL funciona como a base da nossa pilha de tecnologias, garantindo que os dados estejam disponíveis de forma confiável e eficiente para visualização.

## Metabase: A Ferramenta de Visualização

### O que é Metabase?

Metabase é uma plataforma de inteligência de negócios (BI) e visualização de dados de código aberto que permite transformar dados brutos em insights valiosos através de gráficos, tabelas e dashboards interativos - tudo sem necessidade de conhecimento em SQL ou programação.

### Principais características

- **Interface amigável**: Permite criar visualizações complexas com uma interface drag-and-drop
- **Dashboards interativos**: Agrupa múltiplas visualizações em dashboards compartilháveis
- **Múltiplas fontes de dados**: Conecta-se a praticamente qualquer banco de dados SQL
- **Perguntas em linguagem natural**: Permite aos usuários fazer perguntas em linguagem natural que são convertidas em consultas SQL
- **Automação**: Permite agendar relatórios e alertas baseados em dados

### Como o Metabase se encaixa no projeto

No nosso projeto, o Metabase é o componente que dá vida aos dados:

1. **Conexão com o PostgreSQL**: O Metabase se conecta ao PostgreSQL para acessar os dados simulados
2. **Visualização dos dados**: Transforma os dados brutos em gráficos e tabelas facilmente compreensíveis
3. **Criação de dashboards**: Permite criar painéis personalizados mostrando métricas de vendas, tráfego web e outras informações importantes
4. **Interface web**: Fornece uma interface acessível via navegador para interagir com os dados

O Metabase funciona como a "janela" para os nossos dados, tornando-os acessíveis e compreensíveis para usuários de todos os níveis técnicos.

## Nginx: O Servidor Web e Proxy Reverso

### O que é Nginx?

Nginx (pronuncia-se "engine-x") é um servidor web de alto desempenho, que também pode funcionar como proxy reverso, balanceador de carga, cache e mais. Conhecido por sua eficiência e baixo consumo de recursos, o Nginx é usado por muitos dos sites de maior tráfego do mundo.

### Principais características

- **Alta performance**: Capaz de lidar com milhares de conexões simultâneas com uso mínimo de recursos
- **Proxy reverso**: Pode receber solicitações dos clientes e encaminhá-las para outros servidores
- **Balanceamento de carga**: Distribui solicitações entre múltiplos servidores
- **Caching**: Pode armazenar conteúdo estático para diminuir a carga nos servidores de aplicação
- **Segurança**: Inclui recursos para limitar conexões, autenticação básica e mais

### Como o Nginx se encaixa no projeto

No nosso projeto de dashboard, o Nginx desempenha um papel crucial como intermediário:

1. **Proxy reverso**: Recebe as solicitações dos usuários na porta 80 (HTTP padrão) e as encaminha para o Metabase, que está rodando internamente
2. **Camada de segurança**: Adiciona uma camada extra de proteção, ocultando o serviço Metabase diretamente da internet
3. **Ponto único de acesso**: Simplifica o acesso ao sistema, permitindo que os usuários acessem através de uma única URL/porta
4. **Potencial para expansão**: Pode ser facilmente configurado para add SSL/TLS (HTTPS), autenticação básica ou balanceamento de carga

O Nginx atua como o "porteiro" do nosso sistema, gerenciando o tráfego de entrada e saída de forma eficiente e segura.

## Como Estas Tecnologias Trabalham Juntas

No nosso projeto, estas três tecnologias formam uma arquitetura em camadas:

1. **PostgreSQL (Camada de Dados)**: Armazena todos os dados e metadados
2. **Metabase (Camada de Aplicação)**: Processa e visualiza os dados
3. **Nginx (Camada de Apresentação/Acesso)**: Gerencia o acesso ao sistema

O fluxo de dados ocorre da seguinte forma:

1. O serviço gerador de dados Python cria registros simulados e os insere no PostgreSQL
2. O Metabase consulta o PostgreSQL para obter esses dados
3. O Metabase transforma os dados em visualizações e dashboards
4. O usuário acessa o Nginx através do navegador
5. O Nginx encaminha a solicitação para o Metabase
6. O Metabase responde com a interface do usuário e as visualizações
7. O Nginx entrega essa resposta ao usuário

Esta arquitetura em camadas é um exemplo clássico de como aplicações web modernas são estruturadas, com separação clara de responsabilidades entre os componentes.

## Containerização com Docker

A beleza deste projeto está na containerização de cada componente:

- **Container PostgreSQL**: Isola o banco de dados e seus dados
- **Container Metabase**: Encapsula a aplicação de visualização
- **Container Nginx**: Gerencia o acesso web
- **Container Gerador de Dados**: Executa o script Python de geração de dados

Cada container funciona de forma independente, com suas próprias dependências, mas pode se comunicar com os outros containers através da rede Docker. Isso cria um sistema modular, escalável e fácil de implantar.

O Docker Compose orquestra todos esses containers, garantindo que sejam iniciados na ordem correta, com as configurações apropriadas e conectados à mesma rede.

## Autor

Vinicius de Lima, PETCC &copy; 2025
