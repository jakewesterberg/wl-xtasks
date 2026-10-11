# From wl-xcon (formerly wl-expcontroller), for wl-xtasks sessions

## 2026-10-11: open asks from wl-xcon

This is the first handover wl-xcon has sent here; the other sibling repositories received theirs on
2026-08-31. The PI decided on 2026-10-11 to send every open ask from wl-xcon to its siblings now, because
wl-xcon's engine build C (the task object, trials that vary) is being planned and cannot be finished
without the answer to ask 1. Answer in this file under each item, or in this repository's own
`docs/CHECKPOINT.md` (it has none yet; create it), as the other siblings did. Treat this file as a message:
move or delete it when answered.

Two facts about today's state, so nothing below is read as a request you cannot already see the answer to.
Both are from this repository's source and wl-xcon's files as of 2026-10-11.

- This repository holds no tasks and no code: `CLAUDE.md`, `LICENSE`, `README.md`, `wl.yaml`
  (`wl.yaml:26`, "The repository holds no code yet"; `lifecycle: scaffolded`). Its README says tasks are
  "written in wl-xcon's task-definition format" (`README.md:3`).
- wl-xcon holds the tasks today, in `tasks/*.py`, and the provisional allocation, in `tasks/allocation.py`.
  A task module defines exactly one `wl_xcon.task.Trial`; the loader is `_load_trial` in `wl_xcon/cli.py`.
  There is no manifest. Nothing in `wl_xcon/` yet refers to this repository.

### 1. The task object's format (blocks wl-xcon build C)

**Information.** The PI decided on 2026-10-11 that wl-xcon's engine build C defines the task object's
format, in wl-xcon, and that his approval of build C's plan is the agreement. Nothing needs to be
negotiated in advance. When C's plan is approved, wl-xcon will publish the format here by reference.

**What happens to this repository once it exists.** `wl.yaml` and the README point at wl-xcon's definition
(this repository publishes the library, wl-xcon publishes the format). Tasks then move here with XC-108
("Move `tasks/` and the provisional allocation to wl-xtasks", waiting on this repository having a library
to load) and the library pull before a run (XC-150, waiting on this repository holding tasks).

**Asked of wl-xtasks.**
- (a) To adopt that format when tasks move.
- (b) To say now, in this file, if wl-xtasks needs anything of the format that wl-xcon might not think of:
  for example a library layout, a manifest per task, a version rule, or how a task cites
  `docs/references/library.bib` (the `ffeb62f` convention). Anything said before C's plan is approved can
  go into the plan; after, it is a change request.

**What the format will carry, so you are not surprised.**
- Engine spec §3.5: one task object per task module, replacing "exactly one `Trial` per module". It holds
  the trial structures (§13.3), the plans (§13.1), the procedures (§15) and the union of their declared
  parameters, which `Session.set` validates against. The loader, checks, pre-flight, review report and
  simulator take the task object. Spec: https://github.com/jakewesterberg/wl-xcon/blob/main/docs/superpowers/specs/2026-10-07-engine-design.md
  (§3.5, §21, §24).
- XC-288 §4's declarations, which a task author writes and the load-time check enforces:
  - each changeable setting's meaning: clear-cut with a difficulty direction, expected with a direction
    and a context note, or not a difficulty setting (§4.1, required, no default);
  - stages in order, each with an id that lasts across the task's versions and a pass rule written in what
    the rig already counts, naming its denominator (§4.2);
  - what "the item chosen" means and how reaction time is defined, from which event to which (§4.3);
  - the task's content hash, a hash of content and never of the file path (§4.4).
  Spec: https://github.com/jakewesterberg/wl-xcon/blob/main/docs/superpowers/specs/2026-10-10-xc288-training-records-design.md
  (§4, §7). The PI approved it on 2026-10-10.

**Not asked.** No task is to be written or moved here yet. No design of the format is asked of wl-xtasks;
no library layout is imposed in this item. Whether the format's version is checked by a manifest here is
for wl-xtasks to say under (b).

**Blocks:** build C (with I). Engine spec §24 lists "wl-xtasks' agreement on the task object" as C's need;
under the PI's decision that agreement is the approval of C's plan, so this item blocks only if (b) turns
up a need.

### 2. Event codes for build F: `STIMULUS_ON`, `STIMULUS_OFF`, `STIMULUS_CHANGED`, and the anchor code (blocks wl-xcon build F; K for the anchor)

**Who allocates what today, stated as plainly as the sources allow.**
- Ownership: wl-xcon ADR-0007 (accepted 2026-08-31) splits it on decodability versus meaning. wl-preproc
  owns framing, escapes, checksum, DVA encoding and `Marker` 1-255. wl-xtasks owns `TaskEvent` 256-4095,
  `TaskTypeCode` 100+, and task-specific and condition codes 4096-32767. Consequence 2: "wl-xcon allocates
  nothing itself", and a task naming an unregistered code is refused at load.
  https://github.com/jakewesterberg/wl-xcon/blob/main/docs/design/decisions/ADR-0007-event-vocabulary-ownership.md
- This repository's `wl.yaml` publishes `task-event-vocabulary` with stability `planned` (`wl.yaml:31`),
  and says "Nothing else is allocated here yet" (`wl.yaml:54`). So wl-xtasks has allocated nothing.
- wl-preproc agreed on 2026-09-01 that 256-4095 is wl-xtasks'. Its four values there (`FIXATION_ACQUIRED`
  256, `FIXATION_END` 257, `CALIBRATION_START` 258, `CALIBRATION_END` 259) are allocated, never to be
  renumbered, and mirrored in wl-preproc's `wl_preproc/contracts/events.py` until this repository ships
  its own.
- wl-xcon's `tasks/allocation.py` holds a provisional allocation in 4096-32767 only (4096 `FIX_ON` onward:
  target, saccade, outcome reasons 4110-4127, `HEAD_FIXED` 4128, `HEAD_RELEASED` 4129, `PARAM_CHANGED` 4130,
  console controls, and so on). It has no `STIMULUS_*` and no anchor code. It says it lives there "until
  that repository has one", which is XC-108.
- S2 §5.1 planned `STIMULUS_ON` and `STIMULUS_OFF` as `TaskEvent` additions "allocated once, in
  `wl-exptasks`, in one commit" with numbers deliberately unassigned (the same names, before the rename):
  https://github.com/jakewesterberg/wl-xcon/blob/main/docs/superpowers/specs/2026-08-31-S2-event-vocabulary-design.md

**Asked of wl-xtasks.** Allocate, once and in one commit, four codes (engine spec §21, from §8.3 and §8.4):
1. `STIMULUS_ON`, `STIMULUS_OFF`, `STIMULUS_CHANGED`: lab-wide task codes for every task. Which stimulus each
   referred to is in wl-xcon's screen log by frame; a group is one code. Tasks' own onset codes
   (`FIX_ON`, `TARGET_ON`) stay as they are. S2 §5.1 puts the first two in the lab-wide `TaskEvent`
   range 256-4095; `STIMULUS_CHANGED` is new in the engine spec and is assumed to join them. Say if
   you would place them otherwise.
2. The anchor code, a code the continuous mode (engine spec §13.6) strobes about once a second so the
   screen log can place a frame against the recording and confine a miscount to one interval. The spec
   fixes its use but not its range or whether it is one code or a small family; wl-xcon is asking you to
   decide that, with wl-preproc's framing in mind (it consumes the code through the 16-bit protocol).
   Engine spec §21 separately asks wl-preproc to record the continuous mode's shape and anchor codes
   (§13.6, §8.4), so tell wl-preproc's session or wl-xcon's once decided.

Spec: https://github.com/jakewesterberg/wl-xcon/blob/main/docs/superpowers/specs/2026-10-07-engine-design.md
(§8.3, §8.4, §21).

**Not asked.** No renumbering of anything already allocated. No change to wl-preproc's frozen codec: the
spec adds no escape, and the codes ride the existing framing. No codes for the XC-288 training records, which
are not strobed. The existing 4096-32767 reference allocation is not to be reviewed as part of this item; it
moves with XC-108.

**Blocks:** build F (recording: stimulus codes), per engine spec §24, "E; wl-xtasks' codes". The anchor
code is also needed by build K (the continuous mode). Neither is the next build; C comes first.

### 3. Other items wl-xcon's backlog holds against this repository

These ask nothing new today. They are listed so you can see what waits on you.

- **XC-108**: move `tasks/` and `tasks/allocation.py` here. Waits on this repository having a library to
  load. It follows ask 1.
- **XC-150**: the library pull from GitHub before a session's first run (P4d-2b spec §6; the decision is
  that tasks are pulled before a run and offline means the last pulled, after confirmation). It is
  wl-xcon's to build; it waits on tasks existing here.
- **XC-207**: block plans and conditions from the task program or chosen at the rig. Waits on tasks
  existing here, then on the plan format of ask 1.
- **XC-289**: a token economy (tokens earned toward fluid and lost on errors), in wl-xtasks and wl-xcon.
  The PI asked on 2026-10-08 that it be brainstormed with build C's procedures and the reference tasks, and
  built after build E. Its reward path is welfare-critical in wl-xcon. S2 §5.1 already lists
  `TOKEN_AWARDED`, `TOKEN_LOST` and `TOKEN_CASHED` as proposed, unnumbered codes; do not allocate them yet.
- **XC-142**: wl-xcon's own documents and code still say `wl-exptasks` or `wl-mllib` in places. That is
  wl-xcon's to fix; nothing is asked of you.
- **XC-294** and **XC-295** (the reference library's Better BibTeX round trip; the citation scan's handling
  of bare keys of other shapes) are wl-xcon's, but the library is shared with this repository. They ask
  nothing of you unless a task cites a key shaped unlike the library's.

### Closed since the scaffold

- **XC-293**, a convention that tasks here cite wl-xcon's reference library by key
  (`docs/references/library.bib`, ADR-0010): done in this repository by `ffeb62f`, "Cite wl-xcon's reference
  library for a task's science-facing choices" (2026-10-08). Do not re-ask.
- **wl-preproc's agreement that `TaskEvent` 256-4095 is yours** (ADR-0007's pending clause): recorded
  2026-09-01 and reflected in `wl.yaml:46-52` and in wl-preproc's `events.py` docstring. Settled.
- **The manifest's earlier false claim of the whole vocabulary**: corrected here on 2026-08-31 (`wl.yaml`
  lines 38-45).
