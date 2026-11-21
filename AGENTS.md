# halimiz-podcast — project instructions

This file adds repository-specific context to the Derinbay Labs constitution (installed
globally as `~/.claude/CLAUDE.md` or `~/.codex/AGENTS.md`); it never overrides it. `CLAUDE.md`
only imports this file (`@AGENTS.md`); repo-local skills live in `.agents/skills/`.

## Product map

HAL'imiz Ne Olacak? daily AI and technology podcast: published feed, episode pages and publishing tooling (GitHub Pages). Not a Go/Next.js/mobile product: the company stack templates other than the baseline CI do
not apply, and the repo keeps its own workflows beside the baseline ones.

## Repository ownership

| Path | Owner |
|---|---|
| `.github/`, root tooling | devops-engineer |
| everything else | the owning developer named on the issue |

## Metrics

`docs/metrics/outcome.txt` holds one line, the weekly outcome (downloads, active users,
crash-free rate, revenue); a figure not measurable yet is `unavailable`.

## Routines

The podcast runs on Claude cloud routines (scheduled tasks). `agents/<name>.md` holds each
routine's prompt verbatim and `agents/routines.json` lists every routine: trigger id, schedule
(`CRON_TZ=Europe/Istanbul`), model, permission mode, connectors and bound device. The repo is
the source of truth; the live routine must match it.

Daily chain (Istanbul time): AI bulletin 04:47 → NotebookLM audio 05:23 → publish 06:52 (pushes
`inbox/<date>`; `.github/workflows/publish.yml` builds the release, feed and pages) → content
07:36 → YouTube check 07:53 → distribution 08:41 and 12:37 → metrics 23:07. Publish catches up
the previous three days when an episode is missing.

To change a routine:

1. Edit `agents/<name>.md` (and `agents/routines.json` for schedule or model) in a PR; merge it.
2. Apply it to the live routine. A routine without a bound device is updated from a Code
   session with `RemoteTrigger update`. A routine bound to kobe (`bound_device: kobe`) rejects
   API and claude.ai web edits (`routine_bind_update_proof_required`); edit it in Claude
   Desktop on kobe.
3. Check with `python tools/check_routines.py <RemoteTrigger list dump>` that the files and the
   live prompts match.

Kobe-bound routines (NotebookLM, publish, YouTube check, both distributions, metrics) run only
while Claude Desktop is running on kobe and the PC is awake. Desktop quitting on 2026-11-18
suspended them for three days. Keep Desktop starting at login and the PC from sleeping; after
an outage, re-enable the suspended routines and run publish so its catch-up fills the gap.

## Product decisions

Standing CEO decisions (naming, hosting, channels, no-approval rule, marketing) are in
`docs/decisions.md`; read it before changing a routine or the publishing flow.
