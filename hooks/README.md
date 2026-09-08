# hooks

Hooks são **scripts + um gatilho** que o cliente de IA roda em eventos do seu ciclo
de vida (antes/depois de uma tool, no início de sessão, etc.). Diferente de skills e
commands — que são arquivos que o cliente lê sozinho de uma pasta — um hook só roda se
estiver **registrado no settings do cliente**. Copiar o script não basta.

Por isso este diretório tem um manifesto **`hooks/hooks.json`** (flat, na raiz) que
**declara** os bindings, e a CLI (`@nio-cli/cli`) o lê no `init`/`sync`, copia cada
script pro namespace **`hooks/nio/`** sob o diretório do cliente e faz merge
não-destrutivo do binding no `settings.json` do cliente.

## Layout (flat)

```
hooks/
  hooks.json            # manifesto — declara TODOS os bindings
  <script>.py           # os scripts, na raiz de hooks/
```

Não há subpasta por role. Hooks são **sempre de código** — a CLI só os provisiona
quando a seleção inclui o role `dev`.

## Alvo e estado atual

- A CLI (`src/lib/hooks.ts`) só provisiona hooks para o **`claudeTarget`**
  (`~/.claude`, merge no `settings.json`).
- Hoje o `claudeTarget` está **fora de `ALL_TARGETS`** (só OpenCode ativo, decisão
  2026-07-27), então **os hooks não são provisionados por nenhum cliente no
  momento**. O `hooks.json` e os scripts ficam prontos para quando o Claude Code
  voltar à lista ou o modelo de hooks do OpenCode for suportado. Ver
  `docs/nio-cli-alignment.md` §C3.

## Formato do `hooks.json`

```json
{
  "hooks": [
    {
      "id": 1,
      "event": "PreToolUse",
      "matcher": "Bash",
      "description": "O que o hook faz, quando dispara e como pular.",
      "script": "check-comment-length.py",
      "clients": ["claude-code"]
    }
  ]
}
```

| Campo         | Obrigatório | Descrição                                                                                              |
| ------------- | ----------- | ------------------------------------------------------------------------------------------------------ |
| `id`          | não         | Inteiro sequencial estável — chave de telemetria que sobrevive a renames. A CLI aceita ausente.        |
| `event`       | sim         | Evento do ciclo de vida: `PreToolUse`, `PostToolUse`, `SessionStart`, `Stop`, etc.                     |
| `matcher`     | não         | Regex do alvo do evento (ex.: `Bash`, `Write\|Edit`). Eventos sem alvo (ex.: `SessionStart`) omitem.   |
| `description` | não         | O que o hook faz — usado no output da CLI.                                                              |
| `script`      | sim         | Nome do arquivo do script, relativo a `hooks/`.                                                         |
| `clients`     | não         | Surfaces que recebem o hook (`claude-code`, `codex`, `cowork`, `opencode`). Ausente = todos.           |

## Notas

- **Escolha o evento certo pra intenção.** Pra **bloquear** uma ação, use `PreToolUse`
  (o hook roda antes e o `exit 2` cancela a tool). Em `PostToolUse` a tool já rodou —
  serve pra avisar/reagir, não pra impedir.
- O script é invocado como `python3 "<caminho>"` — precisa de **`python3` no PATH**
  (o bit de execução é dispensável).
- O provisionamento é **não-destrutivo e idempotente**: a CLI só mexe nas entradas do
  namespace `hooks/nio/` no `settings.json` — hooks próprios do usuário ficam intactos.
  Renomear/remover um hook aqui remove a entrada correspondente no próximo `sync`.
- Cada script traz um `selftest` (`python3 hooks/<script>.py selftest`).
