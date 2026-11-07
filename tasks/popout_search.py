"""Pop-out search: look to the one disc whose color differs. The lab's first training task.

Designed with the PI on 2026-11-07 (wl-xcon's
`docs/superpowers/specs/2026-11-07-popout-search-design.md`, §3; every number below marked "the
PI's" is his from there). An animal that already fixates reliably learns to look to the odd one of
a ring of discs, by its color alone.

**The trial** (§3.1). The fixation point comes on after the gap between trials; the animal looks
to it within 2.0 s and holds it 0.5 s. Then, on one frame, the discs come on and the fixation
point goes off: that is the go ("there will be no delay between array presentation and fixation
dimming/go cue"). **The next saccade from fixation answers** ("anything other than looking at the
target with the next saccade from fix to the target is an error"): landing on the odd one and
holding it 0.3 s is correct and pays one reward; landing on another disc, landing on empty space
or leaving the odd one before its 0.3 s are errors, and so is leaving the fixation point before
the go (an early saccade). Each error blanks the screen for 2.0 s, no reward, and the trial keeps
its own outcome. No saccade within 1.0 s of the go is no response. A trial starts with 1.0 s of
blank screen, the time between trials.

**The stages** (§3.3), the plan `training`: **Alone**, the odd one alone on the ring; **Fade-in**,
four discs, the three distractors climbing from faint to the odd one's brightness on a staircase;
**Crowd**, every disc at full, from 4 discs up to 12 on a staircase. Within a stage a staircase
steps three right harder, one wrong easier [@levitt1971transformed] (wl-xcon's TSK-32, TSK-33);
between stages the rig suggests a move and the trainer confirms or holds it: up at 80% right of
the last 50 answers at the stage's hardest step, back below 50% of the last 50 (TSK-72).

**The colors** (§3.2): wl-style's isoluminant blue, purple and red and the PI's green, held equal
in macaque cone luminance at 15 cd/m² (`stimuli/isohue.json`, plain data; wl-xcon's COL-37). On
each trial one is the odd one and another fills the distractors, drawn from the pairings the
trainer has pooled; the pool starts small and widens when the rig suggests it and the trainer
picks (TSK-73).

**Every number is a setting the trainer may change in the console** (the PI, 2026-11-07: "i
mean, everything should be adjustable in the console, no?"; wl-xcon's TSK-75): each starts at the
PI's value, and a number stays fixed only with its reason written beside it. The stages' own
values (one disc in Alone, four in Fade-in, the distractors at full in Crowd) are conditions'
values, which a person's live value overrides like any other.

Positions and sizes are degrees of visual angle at their place (the PI, 2026-10-19). Its event
codes are wl-xcon's `tasks/allocation.py`'s, until this repository publishes one.
"""

from pathlib import Path

from wl_xcon.photometry import ColorSet, ColorSetLight, Gray
from wl_xcon.task import (
    BACKGROUND,
    EASIER,
    EXPECTED,
    HARDER,
    NEITHER,
    NOT_DIFFICULTY,
    REMEMBERED,
    SAME,
    SPENT,
    STIMULUS,
    After,
    Array,
    Block,
    ByCriterion,
    Choice,
    Condition,
    Counting,
    Disc,
    Entered,
    Exited,
    Hide,
    Hold,
    Mark,
    Meaning,
    ObjectWindows,
    On,
    Outcome,
    P,
    Param,
    Plan,
    Pool,
    ReactionTime,
    Reward,
    SaccadeOnset,
    SaccadeTo,
    Show,
    Staircase,
    State,
    Steps,
    Stimulus,
    Task,
    Trial,
    Uniform,
    Window,
)

#: **The four colors** (§3.2), as plain data beside this repository's tasks: what each color is,
#: read by a path relative to this file; the rig computes each one's drive on its measured panel.
ISOHUE = ColorSet.load(Path(__file__).resolve().parents[1] / "stimuli" / "isohue.json")
#: Their names, in the file's order: blue, purple, red, green.
COLORS = tuple(ISOHUE.colors)

#: The odd one: a `disc_size` disc (1° to start) at the set's full luminance, `color_luminance`
#: (15 cd/m² to start, the file's own).
ODD = {
    color: Disc(size=P("disc_size"),
                color=ColorSetLight(ISOHUE, color, luminance=P("color_luminance")))
    for color in COLORS
}
#: A distractor: a disc as large at `distractor_fraction` of it, faint to full in Fade-in, full in
#: Crowd.
AMONG = {
    color: Disc(size=P("disc_size"),
                color=ColorSetLight(ISOHUE, color, fraction=P("distractor_fraction"),
                                    luminance=P("color_luminance")))
    for color in COLORS
}

#: **The twelve ordered pairings, the odd one's color first** (§3.2, "A pool of four"), in the
#: colors' order: blue among purple, red, green; purple among blue, red, green; red among blue,
#: purple, green; green among blue, purple, red. The pool's value is the sum of the numbers of
#: those it holds, 1, 2, 4 ... 2048 in this order (wl-xcon's `task.Pool`).
POOL = Pool(
    "pairings",
    tuple((ODD[odd], AMONG[among]) for odd in COLORS for among in COLORS if among != odd),
    odd="odd_color",
    distractor="distractor_color",
)
#: **The pool a run starts with where the trainer picks none**: blue among red and red among blue,
#: the two colors the PI first named ("the isoluminate bluish color and redish color"), so from the
#: first trial the odd one is not always the same color. The trainer picks at the run's start
#: (§3.6).
FIRST_PAIRINGS = POOL.number([(ODD["blue"], AMONG["red"]), (ODD["red"], AMONG["blue"])])

# The fixation point, at the center: a fixed place, since the ring and every window are about it.
FIX = Stimulus("fix", at=(0.0, 0.0), looks=Disc(size=P("fix_size"), color=Gray(P("fix_luminance"))))

#: **The ring** (§3.1): discs `disc_size` across (1° to start) on a true circle `ring_radius` from
#: fixation (8° to start), the odd one object 0 and the ring turned to a new direction every trial,
#: so the odd one is anywhere on it. **At the starts**, twelve discs on the 8° ring are 4.13°
#: apart, so 1.5° windows never overlap. **Over the ranges they can**: on a ring of 8° windows
#: wider than 2.06° would, and on the smallest ring, 4°, twelve discs are 2.07° apart, which the
#: 1.5° windows already overlap at (computed 2026-11-07); wl-xcon's load check warns of it
#: (`crowded-array`), and the trainer keeps them apart.
ARRAY = Stimulus(
    "search",
    # The array's center is the fixation point's, fixed with it.
    at=(0.0, 0.0),
    looks=Array(
        n=P("set_size"),
        radius=P("ring_radius"),
        target=0,
        looks=P("odd_color"),
        among=P("distractor_color"),
        phase=P("array_rotation"),
    ),
)

#: The event codes this task strobes, from wl-xcon's `tasks/allocation.py`.
FIX_ON, SACCADE_ONSET, TARGET_ACQUIRED, ABORT_NO_FIXATION = 4096, 4098, 4099, 4100
ABORT_FIXATION_BREAK, REWARD_COMMANDED, ARRAY_ON, DISTRACTOR_ACQUIRED = 4101, 4102, 4103, 4104
OUTCOME_CORRECT, OUTCOME_WRONG_TARGET, OUTCOME_NO_RESPONSE = 4110, 4113, 4117
OUTCOME_ABORT, OUTCOME_FIXATION_BREAK, OUTCOME_TARGET_BREAK = 4118, 4119, 4120
TIMEOUT_ON = 4138


def _timeout(state: str, outcome: Outcome, reason: int) -> State:
    """**The blank screen after an error** (§3.1, "A short timeout"): nothing shown for `timeout`
    seconds, no reward, then the trial ends with the error's own `outcome`, its reason strobed
    just before the trial's end marker, which several outcomes share."""
    return State(state, go=[On(After(P("timeout")), outcome, do=[Mark(reason)])])


search = Trial(
    start="between",
    # Direct view, with the lab's other search tasks.
    view="direct",
    # Black ("On black, faint to full"): the default bottom layer, `None`.
    background=None,
    # Its counting table: the array appears with the go. A break after it -- a look to empty
    # space, leaving the odd one before its hold -- is spent, used up as a wrong disc's trial is:
    # the PI's rule makes the three one kind of error, each with the timeout (§3.1), and the lab's
    # other pop-out search spends them too (wl-xcon's `tasks/visual_search.py`). A break before the
    # go is owed. Each stage is one condition worked on past its first trial, so neither brings a
    # trial back: the next is drawn afresh.
    counting=Counting(after_stimulus=SPENT, appears="go"),
    windows=[
        Window("fix", at=(0.0, 0.0), radius=P("fix_window"), on="fix"),
        # The same window after the go, the fixation point gone: nothing is drawn there on
        # purpose, and leaving it is the answer's saccade starting.
        Window("center", at=(0.0, 0.0), radius=P("fix_window"), on=REMEMBERED),
        ObjectWindows(of="search", radius=P("object_window")),
    ],
    params=[
        # The PI's starting values (§3.1, "that looks good"), each a value the trainer may change.
        # The ranges are the builder's, wide enough for a trainer and inside what the checks
        # hold (the fix round, 2026-11-07).
        Param("inter_trial", unit="s", low=0.0, high=10.0, start=1.0),
        Param("fix_acquisition", unit="s", low=0.5, high=10.0, start=2.0),
        Param("fix_hold", unit="s", low=0.05, high=2.0, start=0.5),
        Param("response_deadline", unit="s", low=0.1, high=3.0, start=1.0),
        Param("target_hold", unit="s", low=0.05, high=1.0, start=0.3),
        Param("timeout", unit="s", low=0.0, high=10.0, start=2.0),
        # The PI's sizes (§3.1). At the starts, twelve discs on the 8° ring are 4.13° apart, so a
        # window wider than 2.06° would overlap its neighbor's (computed 2026-11-07); over the
        # ranges below they can overlap, which the load check warns of (`crowded-array`).
        Param("fix_window", unit="deg", low=0.5, high=5.0, start=2.0),
        Param("object_window", unit="deg", low=0.5, high=2.0, start=1.5),
        Param("disc_size", unit="deg", low=0.2, high=3.0, start=1.0),
        Param("ring_radius", unit="deg", low=4.0, high=14.0, start=8.0),
        Param("fix_size", unit="deg", low=0.1, high=1.0, start=0.3),
        # The colors' brightness at full, cd/m² of macaque luminance ("15 cd/m² on every rig",
        # §3.2), the color set file's own to start; Fade-in's distractors take a share of it.
        Param("color_luminance", unit="cd/m2", low=1.0, high=30.0,
              start=ISOHUE.luminance_cd_m2),
        # Absolute luminance, D65 white, as the lab's other fixation points (the PI, 2026-10-07).
        Param("fix_luminance", unit="cd/m2", low=0.0, high=80.0, start=40.0),
        # How many discs: one in Alone, four in Fade-in, Crowd's staircase from 4 to 12.
        Param("set_size", unit="objects", low=1, high=12, start=4),
        # The distractors' luminance as a share of the odd one's: Fade-in's staircase from faint;
        # full in Crowd. Its start is the staircase's first level, so Fade-in starts faint.
        Param("distractor_fraction", unit="fraction", low=0.0, high=1.0, start=0.1),
        # Turned to a new direction every trial (`TASK.draws`).
        Param("array_rotation", unit="deg", low=0.0, high=360.0, start=0.0),
        # The two looks each trial's pairing gives, and the pairings pooled.
        Param("odd_color", unit="appearance", choices=tuple(ODD.values())),
        Param("distractor_color", unit="appearance", choices=tuple(AMONG.values())),
        Param("pairings", unit="pairings", low=1, high=4095, start=FIRST_PAIRINGS),
        # **The bars** (§3.4), one pair for every stage: up at 80% right of the last 50 answers
        # at the stage's hardest step, back below 50% of the last 50 first answers ("80%
        # correct, last 50 trials"; "Below 50% of the last 50"), each read at every judgment.
        Param("move_up_bar", unit="fraction", low=0.5, high=1.0, start=0.8),
        Param("move_up_window", unit="answers", low=5, high=200, start=50),
        Param("move_back_bar", unit="fraction", low=0.05, high=0.95, start=0.5),
        Param("move_back_window", unit="answers", low=5, high=200, start=50),
        # **The staircases** (§3.4, "Automatic within a stage"): three right a level harder, one
        # wrong a level easier, in both stages [@levitt1971transformed]; and each stage's step,
        # the distractors by a tenth of full, the discs one at a time ("set size starts at 4, and
        # finer steps"), the builder's (§7).
        Param("staircase_down", unit="answers", low=1, high=10, start=3),
        Param("staircase_up", unit="answers", low=1, high=10, start=1),
        Param("fade_in_step", unit="fraction", low=0.05, high=0.9, start=0.1),
        Param("crowd_step", unit="objects", low=1, high=8, start=1),
    ],
    states=[
        # The time between trials, a blank screen.
        State("between", go=[On(After(P("inter_trial")), "await_fix")]),
        State(
            "await_fix",
            enter=[Show(FIX), Mark(FIX_ON)],
            go=[
                On(Entered("fix"), "hold_fix"),
                On(
                    After(P("fix_acquisition")),
                    Outcome.NO_FIXATION,
                    do=[Mark(ABORT_NO_FIXATION)],
                ),
            ],
        ),
        State(
            "hold_fix",
            go=[
                # **The go**: the discs on and the fixation point off, on one frame.
                On(
                    Hold("fix", P("fix_hold")),
                    "go",
                    do=[Hide("fix"), Show(ARRAY), Mark(ARRAY_ON)],
                ),
                # An early saccade: leaving the fixation point before the go.
                On(
                    Exited("fix"),
                    "early",
                    do=[Hide("fix"), Mark(ABORT_FIXATION_BREAK), Mark(TIMEOUT_ON)],
                ),
                # Longer than any legal `fix_hold`, as the lab's other tasks bound a hold: a bound
                # on a hold the engine runs, no number a trainer sets.
                On(After(10.0), Outcome.NO_FIXATION),
            ],
        ),
        State(
            "go",
            go=[
                # The answer begins: the eye leaves the fixation window, and `flight` scores the
                # saccade where it lands.
                On(Exited("center"), "flight", do=[Mark(SACCADE_ONSET)]),
                On(
                    After(P("response_deadline")),
                    Outcome.NO_RESPONSE,
                    do=[Mark(OUTCOME_NO_RESPONSE)],
                ),
            ],
        ),
        State(
            "flight",
            go=[
                On(SaccadeTo("search.target"), "on_target", do=[Mark(TARGET_ACQUIRED)]),
                On(
                    SaccadeTo("search.distractor"),
                    "wrong",
                    do=[Hide("search"), Mark(DISTRACTOR_ACQUIRED), Mark(TIMEOUT_ON)],
                ),
                # Empty space: the saccade landed on no disc. The saccade in flight as this state
                # began counts here only where it lands; one that begins here is a second look,
                # an error, wherever it goes. An eye that stays put ends on the bound below.
                On(SaccadeOnset(), "astray", do=[Hide("search"), Mark(TIMEOUT_ON)]),
                # Far longer than any saccade lasts: an engineering bound on landing, no number a
                # trainer sets.
                On(After(0.3), "astray", do=[Hide("search"), Mark(TIMEOUT_ON)]),
            ],
        ),
        State(
            "on_target",
            go=[
                On(
                    Hold("search.target", P("target_hold")),
                    Outcome.CORRECT,
                    do=[Mark(OUTCOME_CORRECT), Mark(REWARD_COMMANDED), Reward("reward_correct")],
                ),
                On(Exited("search.target"), "broke", do=[Hide("search"), Mark(TIMEOUT_ON)]),
                # Longer than any legal `target_hold`: a hold runs its own time; a bound, no number
                # a trainer sets.
                On(After(3.0), Outcome.NO_RESPONSE, do=[Mark(OUTCOME_NO_RESPONSE)]),
            ],
        ),
        _timeout("early", Outcome.FIXATION_BREAK, OUTCOME_FIXATION_BREAK),
        _timeout("wrong", Outcome.WRONG_TARGET, OUTCOME_WRONG_TARGET),
        _timeout("astray", Outcome.ABORT, OUTCOME_ABORT),
        _timeout("broke", Outcome.TARGET_BREAK, OUTCOME_TARGET_BREAK),
    ],
)

#: **The stages** (§3.3, "Alone, Fade-in, Crowd"), easiest first. Each is one condition, worked
#: until the trainer moves on; its own value -- one disc, four, the distractors at full -- a
#: condition's, which a person's live value overrides. Each stage's bar is `move_up_bar` right of
#: its last `move_up_window` answers at its hardest step ("80% correct, last 50 trials"; "Hardest
#: step reached, 80% there"). The staircases' floors and ceilings are the stages' own, faint to
#: full and 4 to 12 discs ("set size starts at 4"); their steps and counts are settings. Neither
#: declares where it starts, so each starts at the level nearest the run's value of its setting,
#: which the trainer picks at the run's start.
UP = (P("move_up_bar"), P("move_up_window"))
STEPPED = {"down": P("staircase_down"), "up": P("staircase_up")}
TRAINING = Plan(
    [
        Block("Alone", [Condition("alone", {"set_size": 1}, target=1)], criterion=UP),
        Block(
            "Fade-in",
            [Condition("fade_in", {"set_size": 4}, target=1)],
            criterion=UP,
            staircase=Staircase(
                "distractor_fraction", Steps(0.1, 1.0, P("fade_in_step")), **STEPPED
            ),
        ),
        Block(
            "Crowd",
            [Condition("crowd", {"distractor_fraction": 1.0}, target=1)],
            criterion=UP,
            staircase=Staircase("set_size", Steps(4, 12, P("crowd_step")), **STEPPED),
        ),
    ],
    # "Rig suggests, trainer confirms"; back below `move_back_bar` of the last `move_back_window`
    # ("Below 50% of the last 50").
    order=ByCriterion(fall_back=(P("move_back_bar"), P("move_back_window")), confirm=True),
)

TASK = Task(
    structures={"search": search},
    default="search",
    reaction_time=ReactionTime(
        state="go",
        to=("flight",),
        note=(
            "from the go, the frame the discs appear and the fixation point goes off, to the eye "
            "leaving the fixation window, the answering saccade under way"
        ),
    ),
    choice=Choice(objects=("search.target", "search.distractor"), by="saccade"),
    meanings={
        "inter_trial": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "the blank screen between trials: time, not a judgment")),
        "timeout": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "the blank screen after an error, a consequence: it costs the animal time, and makes "
            "no trial easier or harder")),
        "set_size": Meaning(EXPECTED, STIMULUS, raising=HARDER, note=(
            "more discs are more to look past while the animal learns the odd one; once it finds "
            "the odd one by color, a denser ring can make it stand out more, as in a trained "
            "pop-out search"), overrides=(
            "a training stage: Crowd adds discs as its harder steps (the PI, 2026-11-07)")),
        "distractor_fraction": Meaning(EXPECTED, STIMULUS, raising=HARDER, note=(
            "dimmer distractors let the odd one stand out by brightness; at full they match its "
            "luminance and it differs by color alone. An animal already using color may find "
            "bright distractors no harder")),
        "odd_color": Meaning(NOT_DIFFICULTY, STIMULUS, note=(
            "which of the four colors the odd one takes, drawn from the pool each trial; the four "
            "are equal in macaque luminance, so none is easier by brightness")),
        "distractor_color": Meaning(NOT_DIFFICULTY, STIMULUS, note=(
            "which of the four colors the distractors take, drawn from the pool each trial")),
        "pairings": Meaning(NOT_DIFFICULTY, STIMULUS, note=(
            "which pairings of odd color and distractor color are drawn; widening the pool adds "
            "pairings, not difficulty")),
        "disc_size": Meaning(EXPECTED, STIMULUS, raising=EASIER, note=(
            "larger discs are easier to see and to land a saccade on; the windows are their own "
            "settings")),
        "ring_radius": Meaning(NOT_DIFFICULTY, STIMULUS, note=(
            "how far the ring sits from fixation, as the shared list's array_eccentricity: what "
            "moving it does depends on the search")),
        "fix_size": Meaning(EXPECTED, STIMULUS, raising=EASIER, note=(
            "a larger fixation point is easier to find")),
        "color_luminance": Meaning(EXPECTED, STIMULUS, raising=EASIER, relative_to=BACKGROUND,
                                   note=(
            "brighter discs on black are easier to see, as a target's luminance is; every color "
            "and the distractors' share move together, so the odd one still differs by color "
            "alone at full")),
        "move_up_bar": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "when the rig suggests moving up or widening the pool, not what a trial asks")),
        "move_up_window": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "how many answers the bar to move up reads, not what a trial asks")),
        "move_back_bar": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "when the rig suggests moving back, not what a trial asks")),
        "move_back_window": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "how many first answers the bar to move back reads, not what a trial asks")),
        "staircase_down": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "how many right in a row step the staircase harder, between trials; its level is "
            "the difficulty, not this")),
        "staircase_up": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "how many wrong in a row step the staircase easier, between trials")),
        "fade_in_step": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "how far apart Fade-in's levels are; the level the staircase gives is the difficulty")),
        "crowd_step": Meaning(NOT_DIFFICULTY, NEITHER, note=(
            "how many discs apart Crowd's levels are; the level the staircase gives is the "
            "difficulty")),
    },
    # The rig fixes the head, as the lab's other rig tasks need it.
    needs_fixed_head=True,
    pool=POOL,
    plans={"training": TRAINING},
    # The ring's direction, anywhere, each trial; a trial a drum brings back (should the trainer
    # switch drumming on) keeps its place, as it keeps its pairing.
    draws={"array_rotation": Uniform(0.0, 360.0, repeat=SAME)},
)
