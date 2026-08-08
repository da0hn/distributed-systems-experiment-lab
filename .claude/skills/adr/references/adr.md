# ADR-[NNNN]: [Título curto no imperativo]

- **Estado:** Aceito
- **Data:** [AAAA-MM-DD]
- **Etapa do roadmap:** [N]
- **Relacionado:** [ADR-NNNN ou Não se aplica — motivo.]

[Um ADR nasce `Aceito`: ele registra escolha já feita, e o debate acontece antes, na
linha da fila. Troque por `Proposto` somente quando a pessoa pedir um ADR em debate.
Os estados são os de `docs/adr/README.md`, seção "Estados", e a regra está em
`docs/specification-process.md`, seção "A decisão vem antes do artefato".]

[Os dois campos abaixo entram só quando um ADR posterior alterar este. Omita-os enquanto
nada tiver alterado a decisão. Ver `references/adr-lifecycle.md`, seção "O rastro de
alterações".]

- **Última atualização:** [AAAA-MM-DD]
- **Alterado por:** [ADR-NNNN — substituição | subsunção | emenda | adendo; qual regra,
  com a seção de origem.]

[Um **patch** move só `Última atualização`, e nunca `Alterado por`: patch não é alteração
por outro ADR. Ele é registrado na seção `## Patches aplicados`, no fim do arquivo.]

## Contexto

[Situação, fatos e restrições. Não descreva a solução.]

## Problema

[Pergunta a responder e forças em conflito. Uma força por linha.]

## Decisão

[O que foi decidido. Use voz ativa e presente. Não coloque o motivo, histórico ou
alternativas nesta seção.]

[Quando descrever fluxo, inclua um diagrama Mermaid junto do parágrafo. Use
`sequenceDiagram` para chamadas no tempo e `flowchart` para topologia ou hierarquia.]

## Justificativa

[Por que a decisão foi tomada. Ligue cada motivo a um fato, força ou restrição das
seções anteriores.]

## Consequências

### Positivas

- [O que fica mais fácil.]

### Negativas

- [O custo ou o que fica mais difícil.]

### Neutras

- [O que muda sem valor positivo ou negativo.]

## Trade-offs

- O benefício [X] foi aceito em troca do custo [Y].

## Alternativas consideradas

### [Alternativa A]

**Descartada.** [Argumento legítimo a favor e motivo técnico para descartá-la.]

### [Alternativa B]

**Descartada.** [Argumento legítimo a favor e motivo técnico para descartá-la.]

## Quando esta decisão deixa de valer

[Sinal concreto e observável que exige revisão.]

## Questões em aberto

[Esta seção existe só enquanto o estado for `Proposto`. Num ADR que nasce `Aceito`,
omita-a: a pendência vira linha em `docs/adr/fila-de-decisoes.md`, ou questão própria
em `docs/questions/`, com o identificador que
`docs/questions/README.md`, seção "Identificador", define.]

| # | Questão                | Status |
|---|------------------------|--------|
| 1 | [Resumo em uma linha.] | aberto |

[Use `aberto (crítico)` para risco que produz resultado falso sem falha de teste.
Use `encaminhado` quando outro ADR identificado for responsável. Use `resolvida`
somente quando citar a origem da resolução.]

### 1. [Título da questão]

[Argumento completo. Não deixe uma lacuna apenas na conversa.]

## Patches aplicados

[Esta seção é **obrigatória** e é sempre a **última** do arquivo, desde 2026-08-07 —
depois até de um `## Adendo`. Um ADR sem patch nenhum a carrega assim mesmo, com a linha
"Nenhum patch aplicado.", para que a ausência de patch seja afirmada e não inferida.]

Nenhum patch aplicado.

O regime de patch está em [`README.md`](README.md#a-revogação-da-imutabilidade-decidida-em-2026-08-07).
Um patch conserta citação, caminho ou erro material; ele NÃO DEVE alterar a decisão nem o
argumento que a sustentava.

[Ao aplicar o primeiro patch, troque "Nenhum patch aplicado." pela tabela abaixo, e
acrescente uma linha por patch. Uma linha registrada NÃO DEVE ser removida.]

| Data         | Seção do corpo | O que mudou                     | Por quê                          |
|--------------|----------------|---------------------------------|----------------------------------|
| [AAAA-MM-DD] | [`## Seção`]   | [o texto antigo e o texto novo] | [o defeito que o patch conserta] |
