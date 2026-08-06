# Template do patch de skill

Um patch cobre uma regra e um arquivo alvo. Apresente-o na conversa antes de aplicar.
NÃO DEVE aplicar sem aprovação explícita da pessoa.

Copie a estrutura abaixo, uma vez por patch.

---

## Patch <N> — <o que a regra passa a exigir, em uma frase>

**Arquivo alvo.** `<caminho relativo>`, seção `<título da seção>`.

**Tipo de atrito.** <um dos seis de `taxonomia-de-atrito.md`>.

**Evidência.**

- <caminho:linha, ou sessão `<id>` com o trecho citado>
- <segunda ocorrência, ou a correção explícita da pessoa>

**Limiar.** <duas ocorrências independentes | correção explícita da pessoa>.

**Antes.**

~~~markdown
<trecho atual, literal; escreva "Seção ausente." quando for inclusão>
~~~

**Depois.**

~~~markdown
<trecho proposto, literal>
~~~

**Efeito no orçamento.** <arquivo>: <atual> para <proposto> caracteres, teto <teto>.
<Quando o patch adiciona texto, nomeie o que sai ou por que nada sai.>

**Efeito colateral.** <outra skill, agente ou índice que passa a divergir; escreva
"Nenhum." quando não houver.>

**Memória afetada.** <arquivo de `memory/` a apagar ou reescrever; escreva "Nenhuma."
quando não houver.>

---

## Regras de preenchimento

**A regra é acionável.** Ela nomeia o ator, a ação e a condição. Um patch cujo
"Depois" só acrescenta advérbio ou ênfase é rejeitado.

**O "Antes" é literal.** Copie o texto atual, sem reescrever. Um "Antes" aproximado
esconde o que a mudança de fato faz.

**Um patch não agrupa mudanças independentes.** Duas regras distintas viram dois
patches, ainda que no mesmo arquivo, porque a pessoa pode aprovar uma e rejeitar a
outra.

**O orçamento é medido, não estimado.** Conte os caracteres do arquivo depois da
mudança.

**Patch em ADR aceito não existe.** Nenhum ADR aceito é editado. Quando o atrito
apontar para uma decisão registrada em ADR, o destino é a fila de decisões de
`docs/adr/fila-de-decisoes.md`, e o patch é rejeitado na origem.
