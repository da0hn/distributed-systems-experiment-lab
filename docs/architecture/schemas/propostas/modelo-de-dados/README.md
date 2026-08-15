# Propostas de modelo de dados

Nove desenhos de schema, três por sistema, escritos para serem debatidos e descartados.
**Nada aqui é decisão.** O dono da forma vigente continua sendo
[`architecture/schemas/`](../../README.md#os-dois-esquemas-e-a-fronteira-que-eles-não-atravessam),
e uma proposta adotada só muda alguma coisa quando virar migração escrita e artefato de
decisão.

## Como elas foram escritas, e por que isso importa

**Cada proposta foi escrita por um agente isolado, que não sabia que as outras existiam.**
Um único autor escrevendo três alternativas produz a segunda como reação à primeira —
cobrindo o que ela deixou de fora, evitando o que ela já fez. O resultado parece três
opções e é uma opção com duas sombras. O isolamento custa a comparação, e por isso a
comparação virou artefato separado, escrito depois que as três fecharam, por quem não
escreveu nenhuma.

**Cada proposta modela o sistema na versão final, e não no primeiro passo.** Isso obrigou
cada autor a escolher o que ainda não foi decidido. Toda escolha dessas está declarada na
seção `## Decisões assumidas` da própria proposta, com a alternativa descartada e **o que
muda no modelo se a decisão for a contrária**. Ler essa tabela é ler o preço de adotar
aquele desenho.

**Assumir não é decidir.** Uma linha de `## Decisões assumidas` continua sendo pergunta
aberta do repositório, e nenhuma delas foi fechada por ter sido assumida.

## Índice

| Sistema                                   | O que o desenho governa                                    | Propostas                                                                                                                                                                                                                                                            | Comparação                                    |
|-------------------------------------------|------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------|
| [`system-under-test`](system-under-test/) | o schema `sut`, que o oráculo lê pelo WAL e nunca consulta | [domínio nu](system-under-test/proposta-1-dominio-nu.md), [rastro append-only](system-under-test/proposta-2-rastro-append-only.md), [catálogo de mecanismos](system-under-test/proposta-3-catalogo-de-mecanismos.md)                                                 | [comparação](system-under-test/comparacao.md) |
| [`lab-plane`](lab-plane/)                 | o schema `lab_plane`, hoje vazio, que é o instrumento      | [instrumento amnésico](lab-plane/proposta-1-instrumento-amnesico.md), [plano durável](lab-plane/proposta-2-plano-duravel-execucao-efemera.md), [livro-razão do veredito](lab-plane/proposta-3-livro-razao-do-veredito.md)                                            | [comparação](lab-plane/comparacao.md)         |
| [`lab-journal`](lab-journal/)             | o schema `lab_journal`, hoje vazio, que é o caderno        | [o caderno conhece cada veredito](lab-journal/proposta-1-o-caderno-conhece-cada-veredito.md), [livro-razão endereçado por conteúdo](lab-journal/proposta-2-livro-razao-enderecado-por-conteudo.md), [série de medições](lab-journal/proposta-3-serie-de-medicoes.md) | [comparação](lab-journal/comparacao.md)       |

O `frontend` não tem banco e o módulo `shared` é biblioteca; nenhum dos dois entra aqui.

## O eixo de cada escolha

Cada trio disputa uma coisa só, e a comparação do sistema é dona do argumento inteiro.

| Sistema             | O que as três disputam                                                                                                                                             |
|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `system-under-test` | qual contaminação da medida é inaceitável — estrutura que existe para medir, veredito só como escalar agregado, ou schema que muda entre duas execuções comparadas |
| `lab-plane`         | o que uma queda do instrumento significa para a execução em curso — que ela morreu, que ela é refeita do zero, ou que ela segue comprovável                        |
| `lab-journal`       | onde mora a semântica de um veredito — no DDL, num vocabulário que é dado, ou fora do banco                                                                        |

## Uma decisão precede o debate do caderno

**A composição global dos formatos de veredito não está decidida, e as três propostas do
caderno assumiram composições diferentes para conseguir modelar.** Cada desenho carrega a
assunção dele na estrutura, e nenhum é neutro. Escolher um deles decide aquela pergunta
por via oblíqua — sem argumento próprio, e sem ninguém perceber que a decisão foi tomada.

O argumento completo está no fim da
[comparação do caderno](lab-journal/comparacao.md#a-segunda-pergunta-não-espera-a-escolha-ela-a-precede).
