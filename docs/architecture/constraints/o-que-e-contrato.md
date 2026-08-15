# Contrato é o que atravessa uma fronteira de processo

OpenAPI, AsyncAPI e JSON Schema descrevem o que atravessa uma fronteira de processo, e
nada além disso. Duas consequências, e as duas são normativas.

**O DDL de um serviço NÃO É contrato.** Migração Flyway, tabela, índice e coluna
descrevem o estado interno de um processo, e nenhum outro processo os lê: a
[fronteira de schema](cada-servico-tem-o-proprio-schema.md) torna o esquema privado por
construção. Inventariar DDL como contrato convida exatamente o `SELECT` cruzado que essa
fronteira fecha. O esquema de um serviço é descrito pelas migrações dele.

**Uma rota de proxy do frontend também não é contrato.** Ela é configuração de
roteamento, e não interface publicada por um processo.

**Um contrato nasce quando a interface existir, nunca antes.** Um esquema escrito para
uma API que ninguém expôs documenta uma intenção, e intenção não é interface. Um
consumidor que encontrasse esse esquema não teria como distinguir o que já pode chamar
do que ainda vai existir.

Hoje nenhum serviço publica interface além do `health` e do `info` do Actuator: os
quatro módulos Java contêm só a classe de aplicação. Não há contrato a escrever.
