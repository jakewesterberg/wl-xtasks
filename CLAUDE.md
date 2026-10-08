# CLAUDE.md

## When you change what this package needs, or where it runs

`wl.yaml` at the root of this repository is this package's own declaration to
`wl-orchestrator`. You author it; nobody else does, and nothing generates it yet.

Update it, then run:

    pip install git+https://github.com/jakewesterberg/wl-manifest.git && wl-check

`wl-check` reads only this repository's manifest and fails only on this
repository's faults. It never reads another package, and once installed it
never touches the network — the install is the only step that does.

`wl-manifest` is public, so it needs no credential. It is not on PyPI, and that
name is unclaimed, so `pip install wl-manifest` installs something else.

The moments that require an edit:

| You changed | Update |
|---|---|
| a dependency on software the lab does not write | `third_party` |
| a dependency on another `wl-*` package | `requires` |
| where this software is deployed | `runs_on` |
| what a developer needs in order to work on it | `builds_on` |
| the package's stage, or what it is doing now | `lifecycle`, `status` |

`requires` is the only place an edge between two lab packages is written down
where the other package can see it. The dependency itself lives in
`pyproject.toml`, which nothing outside your repository reads.

A pinned version needs a `why`. The constraint is recoverable from the code;
the reason it exists is not, and it is the only part a future reader cannot
reconstruct.

`wlo stack <machine-class>` builds a real workstation from `runs_on`,
`builds_on` and `third_party` across every package, so a wrong line here puts
wrong software on a real machine. One of the eight original manifests declared
tools its own specs said the repository does not use.

## Before you write a claim about another repository

Open that repository's own documents and read the passage you are relying on.

Every falsehood found while building the registry came from not doing this: a
status copied from a checkpoint that had gone stale, three tool dependencies
read out of a paragraph describing the manual process a tool replaces, a
quotation that appears in no source. A green test suite caught none of them.

For anything beyond this repository — what a package is called elsewhere, what
a machine class needs, which `wl-*` names resolve to nothing — use a
`wl-orchestrator` checkout (`pip install -e ".[dev]"`, editable matters):

    wlo show <slug>     what a package is, and what it is called elsewhere
    wlo stack dws       what a workstation needs, and why
    wlo reconcile       wl-* names in the lab's docs that resolve to nothing
    wlo check .         this repository's manifest, from an orchestrator checkout
    wlo dependents <s>  who breaks if <s> changes what it publishes

Its `docs/known-gaps.md` records what is known broken; `docs/superpowers/specs/`
holds the design and the reasoning.

## When a task's choice rests on the literature

Cite it by key from wl-xcon's library, `docs/references/library.bib` (for example
`[@levitt1971transformed]`), and give the decision an entry in wl-xcon's
`docs/references/decisions.md`; a choice that rests on the PI's word or a rule says so
there instead (the PI, 2026-10-08; wl-xcon's ADR-0010).
