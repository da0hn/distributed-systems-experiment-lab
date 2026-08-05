# Taxonomia de atrito

Seis tipos. Cada um tem sinal observável, evidência exigida e um contraexemplo que o
descarta. O contraexemplo importa mais que o sinal: ele separa instrução defeituosa de
execução defeituosa. Só a primeira vira patch.

## 1. Retrabalho de artefato

**Sinal.** O mesmo arquivo foi editado três vezes ou mais na mesma sessão, e as edições
posteriores desfazem escolhas das anteriores.

**Evidência.** Os caminhos e a ordem das chamadas de edição, com o trecho que mudou de
ideia.

**Destino típico.** Patch na skill que gerou o artefato — em geral, uma regra que só
aparece no fim do fluxo e deveria aparecer antes de escrever.

**Contraexemplo.** Edições que acrescentam conteúdo novo sem desfazer nada. Escrever em
partes não é retrabalho.

## 2. Erro de ferramenta evitável

**Sinal.** `tool_result` com `is_error`. Os casos recorrentes aqui são edição de string
inexistente, caminho errado, e comando escrito para o shell errado.

**Evidência.** A mensagem de erro citada, e a chamada que a produziu.

**Destino típico.** Patch com a precondição que faltava. "Leia o arquivo antes de
editar" é acionável; "tenha cuidado" não é.

**Contraexemplo.** Erro por estado externo — rede fora, arquivo removido por outro
processo, permissão negada pela pessoa. Nenhuma instrução o teria evitado.

## 3. Correção explícita da pessoa

**Sinal.** Um turno curto do usuário logo após uma resposta longa, com negação,
reformulação ou instrução direta. "Não", "na verdade", "já falei", "sempre faça",
"nunca faça".

**Evidência.** O turno citado na íntegra, com o identificador da sessão.

**Destino típico.** Patch, mesmo em ocorrência única. A pessoa não corrige o que não
incomoda — a correção já é o segundo voto.

**Contraexemplo.** Mudança de escopo. "Agora faça outra coisa" é um pedido novo, e não
uma correção do que veio antes.

## 4. Ordem invertida no fluxo

**Sinal.** Um passo posterior invalidou um passo anterior. O caso clássico é escrever o
artefato e só então descobrir a regra que decidiria o formato dele.

**Evidência.** Os dois passos, na ordem em que ocorreram, e o custo do descarte.

**Destino típico.** Patch que move a precondição para antes da ação que ela controla.

**Contraexemplo.** Descoberta genuína. Se o fato só podia ser conhecido depois de
tentar, a ordem não estava errada.

## 5. Lacuna de instrução

**Sinal.** Uma decisão foi tomada sem que nenhuma skill dissesse o que fazer, e a
pessoa não foi consultada. Este tipo viola a regra do `AGENTS.md` de que decisão é
aprovada por pessoa, explicitamente.

**Evidência.** A decisão tomada, e a busca que mostra que nenhuma skill a cobre.

**Destino típico.** Patch que nomeia o destino da lacuna. Quando a lacuna for
arquitetural, o destino é a fila de decisões, e não uma regra nova.

**Contraexemplo.** Silêncio deliberado. Uma skill pode omitir de propósito para deixar
a escolha com a pessoa. Confirme antes de tratar omissão como defeito.

## 6. Excesso de instrução

**Sinal.** Um passo obrigatório da skill não mudou o resultado em nenhuma execução
observada. Ou o contexto compactou, o que aparece como `isCompactSummary` no
transcrito.

**Evidência.** As execuções em que o passo rodou, e o resultado idêntico sem ele.

**Destino típico.** Patch que remove, funde ou move o passo para `references/`. Este é
o único tipo que reduz o orçamento, e por isso costuma financiar os outros.

**Contraexemplo.** Passo de guarda. Uma validação que não falhou ainda não é inútil —
ela existe para o caso que ainda não ocorreu. Remova só quando a guarda for redundante
com outra que já roda.

## Regra comum a todos

Um achado sem evidência citável é descartado, sem exceção. Uma hipótese sobre por que o
atrito aconteceu vai como pergunta em aberto na entrega, e nunca como justificativa de
patch.
