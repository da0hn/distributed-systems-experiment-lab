# Integrações

A matriz é uma só, e cada fronteira declara o **estado** dela. A divisão binária entre
fato e hipótese não modelava "decidido, e ainda não implementado", e por isso deixava
uma decisão aceita parecer especulação.

| Estado                      | O que ele afirma                                                  |
|-----------------------------|-------------------------------------------------------------------|
| `implementado`              | verificável hoje, na árvore versionada ou em repositório nomeado  |
| `decidido/não implementado` | um ADR aceito o fixou, e nada na árvore o executa                 |
| `hipótese`                  | descrito em documento de planejamento, sem decisão que o sustente |
| `bloqueado`                 | decidido, e impedido por uma linha aberta da fila                 |

## Matriz

| Origem   | Destino   | Tipo                    | Operação ou tópico | Finalidade  | Estado   | Contrato                | Autenticação | Confiabilidade | Evidência          |
|----------|-----------|-------------------------|--------------------|-------------|----------|-------------------------|--------------|----------------|--------------------|
| [Origem] | [Destino] | [HTTP, evento ou outro] | [Nome]             | [Propósito] | [Estado] | [Link ou Não se aplica] | [Mecanismo]  | [Garantia]     | [`caminho#âncora`] |

## Decisões pendentes

- [Pergunta, impacto e a linha da fila que a decide.]

---

**Nunca promova hipótese a estado superior sem evidência nova.** A evidência vai por
caminho e âncora GFM; número de linha só quando o alvo não tiver título que a alcance.

O dono da matriz vigente é `docs/architecture/integrations.md`. Este arquivo é o molde
dela, e não uma segunda matriz.
