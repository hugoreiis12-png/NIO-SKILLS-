# Regras — Business Intelligence

Valem para desenvolvimento de dashboards, relatórios e frameworks de métricas no setor de dados.

## Definição de métricas
- Toda métrica tem uma definição única, documentada e acessível a qualquer pessoa do time.
- Numerador e denominador explícitos para taxas e percentuais.
- Quando duas métricas com nomes diferentes medem a mesma coisa, escolha uma e deprecie a outra.
- Métricas de negócio são versionadas: mudanças de definição têm data e registro.

## Dashboards
- Um dashboard responde a uma pergunta central. Mais de três perguntas distintas = dashboards separados.
- Todo visual tem um título afirmativo: "Conversão caiu 15% em março" — não "Conversão por mês".
- Evite pizza com mais de 4 fatias. Prefira barras horizontais para ranking.
- Cores com significado consistente em todo o dashboard (verde = bom, vermelho = ruim, cinza = neutro).
- Filtros globais afetam todos os visuals, salvo exceção explícita documentada.
- Performance: dashboard com mais de 30 segundos de carregamento precisa de otimização de query ou cache.

## Granularidade e agregação
- Declare a granularidade de cada dataset que alimenta o dashboard (uma linha = o quê?).
- Somas de percentuais são quase sempre incorretas. Some numeradores e denominadores separadamente.
- Médias de médias são incorretas para pesos diferentes. Use a média ponderada.
- Agregações que misturam granularidades diferentes devem ser explicitamente documentadas.

## Atualização e confiabilidade
- SLA de atualização definido e monitorado. Se o dado está atrasado, o dashboard informa.
- Dados parciais (dia ainda não fechado, mês em andamento) são sinalizados visualmente.
- Nunca exiba um número sem saber quando ele foi atualizado pela última vez.

## Comunicação com stakeholders
- Relatório entregue sem contexto é um conjunto de números. Adicione a interpretação.
- Use linguagem de negócio, não técnica: "receita por cliente ativo" em vez de "AVG(revenue) WHERE status='active'".
- Quando um número cai, traga a hipótese de causa junto — não apenas o número.
- Limitações e caveats documentados antes de qualquer stakeholder perguntar.
