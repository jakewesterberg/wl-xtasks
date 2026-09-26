# wl-exptasks

The experiment task library: the behavioural tasks animals perform, on the recording rigs and on wl-touchtrain's cage-side kiosk, written in wl-expcontroller's task-definition format, plus the event-code allocation needed to interpret their output. wl-preproc decodes those codes; wl-works renders a page per task. wl-juicer delivers the rewards these tasks command.

Named `wl-mllib` until 2026-09-26. "ml" was MonkeyLogic, which the lab does not run (wl-expcontroller ADR-0005). The old name, and the earlier `wl-bhvtasks`, `wl-bhveval` and `wl-bhvtask`, still resolve here through the registry's aliases, and GitHub redirects the old URL.

## License

Apache-2.0 — see `LICENSE`. Copyright 2026 Jacob A. Westerberg.

Apache-2.0 applied 2026-09-05, matching the rest of the `wl-*` family. ADR-0007 in
`wl-expcontroller` plans to move its `tasks/` and event allocation here, and that move
is only legal because both sides are permissively licensed.
