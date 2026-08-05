@AGENTS.md

## Sobre este arquivo

As instruções deste repositório vivem em [`AGENTS.md`](AGENTS.md), importado na primeira
linha. Edite lá, nunca aqui.

Este arquivo existe porque o Claude Code lê `CLAUDE.md` e não `AGENTS.md`
([documentação](https://code.claude.com/docs/en/memory)). O import `@AGENTS.md` é o
mecanismo que a própria documentação prescreve para repositórios que mantêm uma fonte
única compartilhada com outros agentes. Um symlink teria o mesmo efeito, mas exige
Administrador ou Modo de Desenvolvedor no Windows.

Acrescente abaixo apenas o que for específico do Claude Code — skills, hooks, comandos.
Qualquer instrução que valha para qualquer agente pertence ao `AGENTS.md`.
