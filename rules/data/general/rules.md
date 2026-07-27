# Regras gerais — trabalho com dados

Valem para todas as funções do setor de dados: analistas, cientistas, engenheiros de dados e BI.

## Reprodutibilidade
- Todo trabalho com dados deve ser reproduzível por outra pessoa, em outra máquina.
- Seeds fixadas para qualquer operação aleatória. Seed padrão: `42`.
- Versões de bibliotecas registradas no início de qualquer notebook ou script.
- Paths relativos, nunca absolutos. Configurações em variável de ambiente ou arquivo `.env`.

## Documentação mínima
- Todo dataset manipulado tem um dicionário de dados associado (mesmo que interno).
- Toda análise começa com a pergunta que ela responde e termina com a conclusão.
- Decisões metodológicas (por que esse filtro? por que esse modelo?) são registradas — não ficam apenas na cabeça.

## Qualidade antes de quantidade
- Valide os dados na entrada, não apenas no output.
- Dados com qualidade desconhecida não viram métrica de negócio sem disclaimer explícito.
- Um número errado publicado para a liderança é pior do que nenhum número.

## Granularidade e agregação
- Saiba sempre qual é a granularidade do dado que você está manipulando (uma linha = o quê?).
- Nunca agregar sem entender o que acontece com nulos na agregação.
- Cuidado com GROUP BY que silenciosamente descarta linhas.

## Privacidade e segurança
- Dados pessoais (PII) não aparecem em logs, prints de console ou relatórios públicos.
- Qualquer dado sensível em ambiente de desenvolvimento é anonimizado ou sintético.
- Acesso a dados de produção é auditável — não use credenciais de produção localmente sem necessidade.

## Comunicação de incerteza
- Toda estimativa vem com intervalo de confiança ou margem de erro quando possível.
- Se não for possível quantificar a incerteza, declare qualitativamente: "estimativa preliminar", "sujeito a revisão".
- Nunca comunique um resultado como definitivo quando os dados são parciais ou a metodologia é experimental.
