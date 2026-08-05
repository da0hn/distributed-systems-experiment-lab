# Ciclo de vida de ADR

Use esta referência somente quando a mudança exigir um ADR.

## Antes de criar

- **Escreva o ADR depois de a pessoa tomar a decisão, e crie-o já com estado `Aceito`.**
  Regra adotada em 2026-08-04. O ADR registra escolha feita, e não escolha em debate.
- **Escrever ADR não é obrigatório.** Avalie primeiro se a escolha atende aos quatro
  critérios. Se não atender, o destino é um artefato de `docs/features/`, e nenhum ADR.
- **O debate acontece na fila de decisões, antes do documento.** Toda objeção e
  alternativa descartada vai para a linha da fila, no mesmo turno em que aparece.
- Escreva um ADR somente para alternativa plausível, impacto durável, restrição futura
  ou trade-off relevante.
- Escreva um ADR por vez. Não crie rascunhos antecipados ou em lote.
- Atribua o próximo número da série corrente ao criar o ADR. Use
  `NNNN-titulo-em-kebab-case.md`.
- Cite a série antiga como `arquivo/NNNN`. Nunca edite arquivo histórico.

## Enquanto estiver proposto

O estado `Proposto` continua disponível e deixou de ser o caminho padrão em 2026-08-04.
Use-o somente quando a pessoa pedir um ADR em debate, e não um registro de escolha feita.

- Use `references/adr.md` sem remover seções obrigatórias.
- Registre toda objeção, alternativa descartada ou pendência em `## Questões em aberto`
  no mesmo turno em que surgir.
- Use `aberto` ou `aberto (crítico)` para questão bloqueadora. Use `encaminhado` quando
  outra decisão identificada for responsável. Use `resolvida` somente com a origem da
  resolução.
- Mantenha `## Decisão` com o que foi escolhido. Registre o motivo em `## Justificativa`.
- Declare trade-off explícito, alternativa legítima descartada e sinal observável que
  encerra a validade da decisão.

## Aceite

- Nunca aceite por omissão. Exija aprovação explícita da pessoa responsável.
- Aceite somente sem questões `aberto` ou `aberto (crítico)`.
- Antes de remover `## Questões em aberto`, transporte cada questão `encaminhado`, inteira,
  para um arquivo próprio `Q-NNNN-K.md` em `docs/questions/`, e acrescente a linha dela ao
  índice de `docs/questions/README.md`, no mesmo commit.
- Mova a decisão fechada para `## Decisão` ou `## Consequências` e então remova a seção de
  questões em aberto.

## Depois de aceito

- Nunca edite nem apague o **corpo** de um ADR aceito. Corpo é tudo a partir da primeira
  seção `##`.
- Se uma decisão nova contradisser a antiga, crie ADR novo e marque a antiga como
  `Substituído por ADR-NNNN`.
- Se a regra antiga continuar correta no caso original, use subsunção. O novo ADR DEVE
  citar a regra e seção originais, declarar o caso que permanece válido e não contradizê-la.
- O ADR subsumido permanece `Aceito`, e o corpo dele permanece intocado.

### O rastro de alterações, obrigatório desde 2026-08-04

Todo ADR alterado — por substituição ou por subsunção — recebe dois campos no
**cabeçalho**, logo depois de `Aceito em:`:

```markdown
- **Última atualização:** AAAA-MM-DD
- **Alterado por:** [ADR-NNNN](NNNN-titulo.md) — substituição | subsunção; qual regra,
  com a seção de origem.
```

- Escreva os dois campos **no mesmo commit** em que o ADR novo nasce.
- `Última atualização` é quando o rastro entrou. `Data` é quando a decisão foi tomada, e
  nunca muda.
- Acumule linhas em `Alterado por` quando houver mais de uma alteração. Nunca remova a
  linha antiga.
- Nomeie **qual regra** e **de qual seção**. Uma referência sem a regra não resolve o
  problema que o campo existe para resolver.

O detalhamento e a justificativa estão em `docs/adr/README.md`, seção "O rastro de
alterações, emendado em 2026-08-04".
