# Plano de escrita dos ADRs do Lote E

**Reduzido em 2026-08-11, e o que sobrou é lápide.** Nasceu em 2026-08-06 como insumo de
escrita, com a própria instrução de fim: "quando os três existirem e os cards estiverem
reconciliados, apague este arquivo".

**Os três existem, e o arquivo não pôde ser apagado.** A
[consulta reversa](../AGENTS.md#antes-de-reduzir-um-documento) apontou três headings
citados de fora, dois deles do
[ADR-0015](0015-a-chave-o-discriminador-de-execucao-e-as-colunas-de-tempo.md), que é
`Aceito` e cujo corpo só muda por patch. Saiu a redação dos ADRs 0010 a 0014, que hoje
vive neles; fica o que a citação alcança.

**Nada aqui é vigente.** O [índice](README.md#índice) é dono do inventário.

## Estado

**Este retrato é de 2026-08-06, e não foi atualizado quando a decisão mudou.** O
`ADR-0015` — e, antes dele, o `ADR-0013` — nasceram `Aceito` depois desta seção,
contrariando a frase abaixo e "deixaram de ser destino de ADR" mais adiante. O `ADR-0015`
registra a contradição e a resolução no próprio cabeçalho, no campo `Divergência de
artefato`, e no fecho de
[`E-55`](fila-de-decisoes.md#e-55-fecha-na-divisão-entre-o-adr-e-um-documento-de-arquitetura-escolhida-em-2026-08-11).
A tabela de três abaixo descreve 2026-08-06, e não hoje.

**O Lote E produz três ADRs, e não seis.** A primeira contagem era inflação: ADR serve a
**alteração permanente e de impacto**, e não a toda escolha fechada. A redução foi decidida
em 2026-08-06, reaplicando os quatro critérios com esse rigor.

| Nº     | Título                                                         | Absorve                                        | Estado     |
|--------|----------------------------------------------------------------|------------------------------------------------|------------|
| `0010` | A fronteira de schema e o CDC como fonte do veredito           | `E-18`, `E-19`                                 | a escrever |
| `0011` | A topologia de serviços e o caderno de laboratório fora do Git | `E-14` a `E-17`, `E-20`, `E-11`, `E-24`        | a escrever |
| `0012` | O broker no caminho do veredito, e a dispensa que ele exigiu   | `E-12`, e a parte permanente de `E-28`, `E-29` | a escrever |

`0010` é premissa de `0012`. Os dois primeiros são obrigatórios pela regra `B-4`, porque
contradizem ADR aceito.

### O que a redução cortou, e para onde cada coisa foi

| Era candidato a ADR                   | Por que não sobrevive               | Vai para                  |
|---------------------------------------|-------------------------------------|---------------------------|
| o alcance por papel do valor          | já vive no `AGENTS.md` como regra   | um parágrafo de porquê lá |
| a identidade derivada da semente      | criar um serviço é topologia        | o `0011`                  |
| a chave, o discriminador e o tempo    | esquema não é arquitetura duradoura | a migração `V2` e o card  |
| qual conector, qual sink, como contar | implementação                       | a configuração e o card   |

**O `0011` cresceu.** Ele absorve o componente de identidade derivada da semente (`E-11`,
`E-24`), porque criar um serviço é decisão de topologia, e a topologia é o assunto dele. A
seção `## ADR-0014` abaixo permanece como insumo — leia-a ao escrever o `0011`, e não como
ADR próprio.

**O `0012` encolheu.** Ele registra o broker no caminho do veredito, o argumento do LSN
que torna a escolha defensável, e a **dispensa explícita da regra de tecnologia** — que é
o que tem impacto permanente, porque define o que pode entrar na stack daqui em diante. A
seção `## ADR-0012` abaixo carrega mais do que o ADR deve conter; use só a parte
permanente, e leve o resto ao card e à configuração.

**As seções `## ADR-0013` e `## ADR-0015` abaixo continuam válidas como conteúdo**, e
deixaram de ser destino de ADR. Elas alimentam o `AGENTS.md`, a migração e os cards.

**Fora dos três, e por quê.** `E-16` escolheu o nome `lab-journal` — nome de serviço não
atende a nenhum dos quatro critérios. `E-32` decidiu a forma de um teste, e o artefato
dela é o próprio teste. A entrega (`E-1` a `E-7`, `E-21`, `E-31`) fica de fora enquanto
`E-3` e `E-31` estiverem abertas: um ADR escrito hoje registraria metade da decisão.

---

---

## ADR-0015 — A chave, o discriminador de execução e as colunas de tempo

**Lápide.** O heading permanece porque o `## O que este ADR desfaz fora de si` do
[ADR-0015](0015-a-chave-o-discriminador-de-execucao-e-as-colunas-de-tempo.md#o-que-este-adr-desfaz-fora-de-si)
o cita, e o corpo de um ADR aceito só muda por patch.

A subseção `### A decisão` era retrato de 2026-08-06 e já apontava para
[`schemas/sut.md`](../architecture/schemas/sut.md#o-schema-do-sistema-medido-sut), dono único da
forma das tabelas desde o fecho de
[`E-55`](fila-de-decisoes.md#e-55-fecha-na-divisão-entre-o-adr-e-um-documento-de-arquitetura-escolhida-em-2026-08-11);
`### O DDL que a decisão produz` já fora apagada pelo commit do próprio ADR-0015. O que o
ADR restringe está no
[corpo dele](0015-a-chave-o-discriminador-de-execucao-e-as-colunas-de-tempo.md#decisão).

As linhas de origem eram `E-9`, `E-10`, `E-22`, `E-23`, `E-25`, `E-26` e `E-27`, e a poda
delas está **bloqueada** por
[`E-76`](fila-de-decisoes.md#e-76--a-poda-do-tema-do-adr-0015-apagaria-regra-que-o-próprio-adr-delega-à-fila).
