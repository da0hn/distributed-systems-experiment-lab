# Aprofundamento

Como aprofundar com segurança um cluster de módulos rasos, dadas as dependências dele.
Assume o vocabulário de [SKILL.md](../SKILL.md) — **módulo**, **interface**, **seam**,
**adaptador**.

## Categorias de dependência

Ao avaliar um candidato a aprofundamento, classifique as dependências dele. A categoria
determina como o módulo aprofundado é testado através do seam.

### 1. Em processo

Computação pura, estado em memória, sem I/O. Sempre aprofundável — junte os módulos e
teste através da nova interface diretamente. Nenhum adaptador é necessário.

### 2. Substituível localmente

Dependências que têm substitutos locais de teste (PGLite para Postgres, sistema de
arquivos em memória). Aprofundável se o substituto existir. O módulo aprofundado é
testado com o substituto rodando na suíte de testes. O seam é interno; não há porta na
interface externa do módulo.

### 3. Remota, mas própria (Portas e Adaptadores)

Serviços seus através de uma fronteira de rede (microsserviços, APIs internas). Defina
uma **porta** (interface) no seam. O módulo profundo é dono da lógica; o transporte é
injetado como **adaptador**. Testes usam um adaptador em memória. Produção usa um
adaptador HTTP, gRPC ou de fila.

Formato da recomendação: *"Defina uma porta no seam, implemente um adaptador HTTP para
produção e um adaptador em memória para teste, para a lógica ficar num módulo profundo só
mesmo estando implantada através de uma rede."*

### 4. Externa de verdade (Mock)

Serviços de terceiros (Stripe, Twilio etc.) que você não controla. O módulo aprofundado
recebe a dependência externa como uma porta injetada; os testes fornecem um adaptador
mock.

## Disciplina de seam

- **Um adaptador é um seam hipotético. Dois adaptadores é um seam real.** Não introduza
  uma porta a menos que pelo menos dois adaptadores se justifiquem (tipicamente produção
  e teste). Um seam com um adaptador só é apenas indireção.
- **Seams internos contra seams externos.** Um módulo profundo pode ter seams internos
  (privados à implementação, usados pelos próprios testes dele) além do seam externo na
  interface. Não exponha seams internos pela interface só porque os testes os usam.

## Estratégia de teste: substitua, não empilhe

- Testes unitários antigos sobre módulos rasos viram desperdício assim que existirem
  testes na interface do módulo aprofundado — apague-os.
- Escreva testes novos na interface do módulo aprofundado. **A interface é a superfície
  de teste.**
- Testes verificam resultados observáveis através da interface, não estado interno.
- Testes precisam sobreviver a refatorações internas — eles descrevem comportamento, não
  implementação. Se um teste precisa mudar quando a implementação muda, ele está testando
  além da interface.
