# Os dois esquemas, e a fronteira que eles não atravessam

Dona única da forma de **dois** schemas — `sut` e `lab_plane` —, e não dos três que o
repositório tem: `lab_journal` fica fora, porque o
[ADR-0011](../../adr/0011-a-topologia-de-servicos-e-o-caderno-de-laboratorio-fora-do-git.md#o-caderno-de-laboratório-sai-do-git)
pôs a definição e o resultado de experimento lá. A forma dele não tem dono enquanto
[`E-57`](../../adr/fila-de-decisoes.md#e-57--a-definição-de-experimento-tem-dois-donos-declarados)
não fechar. **Nenhum documento vigente carrega DDL** e a exceção é `docs/adr/arquivo/`
inteiro, congelado — as duas coisas são do fecho de
[`E-55`](../../adr/fila-de-decisoes.md#e-55-fecha-na-divisão-entre-o-adr-e-um-documento-de-arquitetura-escolhida-em-2026-08-11).
Vários arquivos de lá carregam bloco SQL, entre eles a
[proposta de modelo de dados](../../adr/arquivo/proposta-2026-08-03/modelo-de-dados.md#1-o-esquema-do-system-under-test).

**Nada aqui é decisão nova.** Cada afirmação cita onde a escolha foi fechada, e o que não
foi decidido fica como `Pergunta em aberto`. Esta página também não é contrato — o DDL de
um serviço saiu do inventário por regra própria, em
[`contracts/README.md`](../../contracts/README.md#o-ddl-de-um-serviço-não-é-contrato).

**O dono único é esta pasta, e não um arquivo.** O fecho de
[`E-78`](../../adr/fila-de-decisoes.md#e-78--o-esquemasmd-vira-pasta-com-um-arquivo-por-serviço)
mudou a granularidade em 2026-08-12, e não a decisão: o que `E-55` fixou — que existe um
dono único da forma das tabelas — continua valendo, e o dono passou a ser o diretório. A
fronteira entre os dois schemas não pertence a nenhum dos dois lados, e por isso ela vive
neste `README.md`, e não num deles.

| Arquivo                        | De que ele é dono                                                |
|--------------------------------|------------------------------------------------------------------|
| [`sut.md`](sut.md)             | a forma do schema do sistema medido                              |
| [`lab-plane.md`](lab-plane.md) | a forma do schema do instrumento                                 |
| este `README.md`               | a fronteira entre os dois, e o porquê da forma viver nesta pasta |

**O `lab_journal` não tem arquivo aqui, e a ausência é deliberada.** Criar um arquivo vazio
afirmaria que existe forma decidida a documentar; ele nasce quando
[`E-57`](../../adr/fila-de-decisoes.md#e-57--a-definição-de-experimento-tem-dois-donos-declarados)
fechar.

## Por que a forma vive aqui, e não dentro do ADR-0015

Decidido pela pessoa em 2026-08-11, no fecho de
[`E-55`](../../adr/fila-de-decisoes.md#e-55-fecha-na-divisão-entre-o-adr-e-um-documento-de-arquitetura-escolhida-em-2026-08-11).
O [ADR-0015](../../adr/0015-a-chave-o-discriminador-de-execucao-e-as-colunas-de-tempo.md#decisão)
fica com o que restringe **como o instrumento mede**; a forma desce para cá.

O motivo é o ciclo de vida: o corpo de um ADR aceito só muda por cerimônia de
[lifecycle](../../adr/README.md#a-revogação-da-imutabilidade-decidida-em-2026-08-07),
e o esquema muda antes disso — `version` entra quando `OPTIMISTIC` nascer, como o
[ADR-0006](../../adr/0006-a-forma-da-estrategia-de-concorrencia.md#decisão) e o comentário da
`V1` do sistema medido já anunciam
(`system-under-test/src/main/resources/db/migration/V1__criar_schema_do_sut.sql:5-7`, por
linha, porque o alvo não tem título).

| Alternativa descartada em 2026-08-11 | Por que ela perdeu                                                                                             |
|--------------------------------------|----------------------------------------------------------------------------------------------------------------|
| o diagrama dentro dos Feature Cards  | duas capacidades tocam o schema medido, e o mesmo desenho apareceria duas vezes, livre para divergir, sem dono |
| o diagrama dentro do ADR-0015        | o corpo de um ADR aceito só muda por cerimônia de lifecycle, e o esquema muda antes dela                       |
| um bloco SQL ilustrativo ao lado     | criaria um segundo lugar onde a forma da tabela vive, e os dois divergiriam                                    |

**Manter os dois diagramas desta página equalizados com a migração é mecânico, e não
confiança na memória de quem editar.** `scripts/check_schema_sync.py` compara nome de
tabela entre cada `erDiagram` abaixo e as migrações Flyway do serviço correspondente,
com baseline própria para divergência deliberada — decidido em
[`E-65`, fecho](../../adr/fila-de-decisoes.md#e-65-fecha-no-script-de-nome-de-tabela-escolhida-em-2026-08-11).
O script ainda não existe.

## A ausência de linha entre os dois diagramas é a decisão

Os dois esquemas são desenhados em canvas separados, **e nunca num só**. Um canvas único,
com uma linha ligando `partition_id` a `execution_id`, renderiza uma chave estrangeira que
a fronteira do
[ADR-0010](../../adr/0010-a-fronteira-de-schema-e-o-cdc-como-fonte-do-veredito.md#decisão)
proíbe: nenhuma constraint liga os dois nomes, e nenhuma poderia ligá-los.

O mesmo valor carrega dois nomes de propósito, e quem traduz é um ponto único — o
consumidor de CDC, dentro do `lab-plane`. A tradução vive no
[ADR-0015](../../adr/0015-a-chave-o-discriminador-de-execucao-e-as-colunas-de-tempo.md#o-nome-assimétrico-do-discriminador-e-a-tradução-num-ponto-único),
porque decorre da fronteira, e não da forma da tabela.

## O que muda esta pasta

- a coluna `version`, quando a estratégia `OPTIMISTIC` nascer;
- a forma da tabela de execuções ativas, quando `E-35` e `E-50` fecharem;
- onde a definição de experimento vive, quando `E-57` fechar.

Uma mudança aqui **NÃO DEVE** alterar o ADR-0015. Se ela mudar como o instrumento mede,
é decisão arquitetural nova, e entra na
[fila](../../adr/fila-de-decisoes.md#o-que-esta-fila-enfileira).
