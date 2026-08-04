# Projetando duas vezes

Quando o usuário quiser explorar interfaces alternativas para um candidato a
aprofundamento já escolhido, use este padrão de sub-agentes em paralelo. Baseado em
"Design It Twice" (Ousterhout) — a primeira ideia dificilmente é a melhor.

Usa o vocabulário de [SKILL.md](../SKILL.md) — **módulo**, **interface**, **seam**,
**adaptador**, **alavancagem**.

## Processo

### 1. Enquadre o espaço do problema

Antes de subir sub-agentes, escreva uma explicação, voltada ao usuário, do espaço do
problema para o candidato escolhido:

- As restrições que qualquer interface nova precisaria satisfazer.
- As dependências das quais ela dependeria, e em qual categoria elas caem (veja
  [references/deepening.md](deepening.md)).
- Um esboço de código ilustrativo, aproximado, para dar concretude às restrições — não é
  uma proposta, é só um jeito de tornar as restrições concretas.

Mostre isto ao usuário e prossiga imediatamente para o Passo 2. O usuário lê e pensa
enquanto os sub-agentes trabalham em paralelo.

### 2. Suba sub-agentes

Suba 3 ou mais sub-agentes em paralelo, usando a ferramenta Agent. Cada um precisa
produzir uma interface **radicalmente diferente** para o módulo aprofundado.

Dê a cada sub-agente um briefing técnico separado (caminhos de arquivo, detalhes de
acoplamento, categoria de dependência de [references/deepening.md](deepening.md), o que
fica atrás do seam). O briefing é independente da explicação do espaço do problema,
voltada ao usuário, do Passo 1. Dê a cada agente uma restrição de design diferente:

- Agente 1: "Minimize a interface — mire em 1 a 3 pontos de entrada no máximo. Maximize
  a alavancagem por ponto de entrada."
- Agente 2: "Maximize a flexibilidade — suporte muitos casos de uso e extensão."
- Agente 3: "Otimize para quem chama com mais frequência — torne o caso padrão trivial."
- Agente 4 (se aplicável): "Desenhe em torno de portas e adaptadores para dependências
  que atravessam o seam."

Inclua tanto o vocabulário de [SKILL.md](../SKILL.md) quanto o de `docs/CONTEXT.md` no
briefing, para cada sub-agente nomear as coisas de forma consistente com a linguagem de
arquitetura e a linguagem de domínio do projeto.

Cada sub-agente entrega:

1. Interface (tipos, métodos, parâmetros — mais invariantes, ordem, modos de erro).
2. Exemplo de uso mostrando como quem chama usa a interface.
3. O que a implementação esconde atrás do seam.
4. Estratégia de dependência e adaptadores (veja
   [references/deepening.md](deepening.md)).
5. Trade-offs — onde a alavancagem é alta, onde ela é rasa.

### 3. Apresente e compare

Apresente os desenhos em sequência, para o usuário absorver cada um, depois compare-os em
prosa. Contraste por **profundidade** (alavancagem na interface), **localidade** (onde a
mudança se concentra) e **posição do seam**.

Depois de comparar, dê sua própria recomendação: qual desenho você acha mais forte e por
quê. Se elementos de desenhos diferentes se combinariam bem, proponha um híbrido. Seja
opinativo — o usuário quer uma leitura forte, não um cardápio.
