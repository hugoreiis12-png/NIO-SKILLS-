# Política de segurança

## O que este repositório contém

`@nio-cli/skills` é **conteúdo**: Markdown (`SKILL.md`, `AGENTS.md`, rules,
commands, agents), JSON de contrato, e scripts de manutenção (`scripts/`,
`hooks/`) que rodam **só no CI e no pre-push**.

**O repositório não executa nada de um agente.** A NIO-CLI que o consome
**copia arquivos** — nunca importa nem roda código de skill.

## A camada NOOA (opcional)

Uma skill pode trazer uma camada executável opcional — um pacote Python
(`<skill>/nio_skill_<id>/`) que expõe um `nooa.Skill`. Ver
[`docs/nooa-integration.md`](docs/nooa-integration.md).

- **Nunca executada pelo repo nem pela NIO-CLI.** O CI (`nooa-layer-check`)
  apenas **importa** os pacotes num runner efêmero — nunca instancia um agente,
  nunca roda um `CodeActStrategy`.
- **A execução acontece só num host NOOA, que DEVE rodar em isolamento de SO**
  (container, VM, ou [NVIDIA OpenShell](https://github.com/NVIDIA/OpenShell)).
  O NOOA executa Python gerado por LLM; os validadores AST + denylist dele são
  defesa em profundidade, **não** contenção.
- **Sem segredos no repositório.** Ferramentas que precisam de credencial as
  recebem do ambiente do host — nunca hardcoded, nunca em `.env` versionado,
  nunca via `${VAR}` em config.
- **Superfície mínima.** Operação destrutiva vai embrulhada em método estreito;
  `@slash_command(user_only=True)` impede o LLM de invocá-la.
- **Carrega inativa.** O host descobre a camada mas só a ativa por opt-in
  explícito do usuário.

## Dependências

`nooa` é pinado a uma tag git exata (`nio-skills.json` → `nooa_version`). Bump é
deliberado e passa pelo CI. Nenhuma dependência com faixa aberta.

## Reportar uma vulnerabilidade

Abra um [private security advisory](https://github.com/hugoreiis12-png/NIO-SKILLS-/security/advisories/new)
no GitHub. Não abra issue pública para vulnerabilidades.
