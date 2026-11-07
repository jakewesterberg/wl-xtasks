# wl-xtasks

The experiment task library: the behavioural tasks animals perform, on the recording rigs and on wl-touchtrain's cage-side kiosk, written in wl-xcon's task-definition format, plus the event-code allocation needed to interpret their output. wl-preproc decodes those codes; wl-works renders a page per task. wl-juicer delivers the rewards these tasks command.

Named `wl-exptasks` until 2026-09-28, `wl-mllib` before that until 2026-09-26. "ml" was MonkeyLogic, which the lab does not run (wl-xcon ADR-0005). The old names, and the earlier `wl-bhvtasks`, `wl-bhveval` and `wl-bhvtask`, still resolve here through the registry's aliases, and GitHub redirects the old URLs.

## Layout

- `tasks/` holds the tasks, one Python file each in wl-xcon's task-definition format, each defining exactly one `Task`. wl-xcon reads a task by its path (`wlx check`, `wlx review`, `wlx run`) until its library pull exists (wl-xcon's XC-150), and tests it in `tests/test_popout_search.py` through a checkout of this repository. The first is `tasks/popout_search.py`, the pop-out search, designed with the PI on 2026-11-07 (wl-xcon's `docs/superpowers/specs/2026-11-07-popout-search-design.md`).
- `stimuli/` holds what a task's stimuli are, as plain data that needs no wl-xcon code to read. `stimuli/isohue.json` is four colors held equal in macaque cone luminance, from wl-style's isohue spectrum; its `source` says where each number came from. A task reads its file by a path relative to its own, and the rig computes each color's drive values on its measured panel.
- The event codes the tasks strobe are wl-xcon's `tasks/allocation.py`'s until this repository publishes its own allocation (`task-event-vocabulary` in `wl.yaml`).

## License

Apache-2.0 — see `LICENSE`. Copyright 2026 Jacob A. Westerberg.

Apache-2.0 applied 2026-09-05, matching the rest of the `wl-*` family. ADR-0007 in
`wl-xcon` plans to move its `tasks/` and event allocation here, and that move
is only legal because both sides are permissively licensed.
