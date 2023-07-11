# 1. Contexto do Problema de Negócio
O objetivo deste dashboard/analise exploratória é ajudar o CEO a identificar pontos chaves da empresa, respondendo às perguntas que ele fizer utilizando dados.

A empresa fictícia Fome Zero é um marketplace de restaurantes, seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.

# 2. O Desafio
O CEO foi recém contratado e precisa entender melhor o negócio para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais o negócio, e para isso, ele precisa que seja feita uma análise nos dados da empresa e que sejam gerados dashboards, a partir dessas análises, para responder às seguintes perguntas:

### 2.1 Visão Geral
  1. Quantos restaurantes únicos estão registrados?
  2. Quantos países únicos estão registrados?
  3. Quantas cidades únicas estão registradas?
  4. Qual o total de avaliações feitas?
  5. Qual o total de tipos de culinária registrados?
  6. Uma visão geral da distribuição dos restaurantes e suas principais métricas.
  
### 2.2 Visão Pais
  1. Qual a quantidade de restaurantes por pais?
  2. Qual a quantidade de cidades avaliadas por pais?
  3. Quantidade de Avaliações feitas por pais?
  4. Qual a média de preço por um prato para duas pessoas?
  5. Quais são os paises que posuem as melhores médias de avaliações?
  6. Quais são os paises que posuem os piores médias de avaliações?
  
### 2.3 Visão Cidades
  1. Quais são as cidades que mais possuem restaurantes?
  2. Quais são as cidades que tem sua avaliação média acima de 4?
  3. Quais são as cidades que tem sua avaliação média menor que 2.5?
  4. Quais são as cidades que tem a maior quantidade de culinárias?
  
### 2.4 Visão Culinária
  1. Quais são os melhores restaurantes dos principais tipos de culinárias?
  2. Quais são os melhores restaurantes?
  3. Quais são os melhores tipos de culinárias?
  4. Quais são os piores tipos de culinárias?
  
# 3. Premissas assumidas para a análise
  1. Desconsiderado notas iguais a zero.
  2. Desconsiderado valor médio por prato para duas pessoas iguais a zero.
  3. Os valores dos pratos para duas pessoas estão dolarizados utilizando a cotação do dia 21/06/2023.
  4. Esta sendo considerado que todos os clientes votaram.
  5. O painel estratégico foi desenvolvido utilizando as métricas que refletem as 4 principais visões do modelo de negócio da empresa.
  
# 4. O produto Final do Projeto
  Painel online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet.
  O painel pode ser acessado através desse link: https://dslucasribeiro-fomezero.streamlit.app

# 5. Conclusões
  O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.
  Da visão Geral podemos ver que o principal mercado do marketplace está localizado nos Estados Unidos e India.

# 6. Próximo Passos
	Calcular a receita gerada por cada Pais
	Criar novos filtros
 	Validar Hipóteses

