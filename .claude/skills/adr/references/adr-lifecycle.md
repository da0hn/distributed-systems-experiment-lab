# Ciclo de vida de ADR

Use esta referência somente quando a mudança exigir um ADR.

## Antes de criar

- Escreva um ADR somente para alternativa plausível, impacto durável, restrição futura
  ou trade-off relevante.
- Escreva um ADR por vez. Não crie rascunhos antecipados ou em lote.
- Atribua o próximo número da série corrente ao criar o ADR. Use
  `NNNN-titulo-em-kebab-case.md`.
- Cite a série antiga como `arquivo/NNNN`. Nunca edite arquivo histórico.

## Enquanto estiver proposto

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

- Nunca edite ou apague um ADR aceito.
- Se uma decisão nova contradisser a antiga, crie ADR novo e marque a antiga como
  `Substituído por ADR-NNNN`.
- Se a regra antiga continuar correta no caso original, use subsunção. O novo ADR DEVE
  citar a regra e seção originais, declarar o caso que permanece válido e não contradizê-la.
- Não altere o texto do ADR subsumido. Ele permanece `Aceito`.
