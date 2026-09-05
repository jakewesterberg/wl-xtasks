# wl-mllib

The MonkeyLogic task library: the behavioural tasks animals perform in experiments, plus the event-code allocation needed to decode their output. wl-preproc reads event handling from here rather than defining it; wl-works renders a page per task. wl-shook and wl-juicer are devices these tasks drive.

## License

Apache-2.0 — see `LICENSE`. Copyright 2026 Jacob A. Westerberg.

Apache-2.0 applied 2026-09-05, matching the rest of the `wl-*` family. ADR-0007 in
`wl-expcontroller` plans to move its `tasks/` and event allocation here, and that move
is only legal because both sides are permissively licensed.
