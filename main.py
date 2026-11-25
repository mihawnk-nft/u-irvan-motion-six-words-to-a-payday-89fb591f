# Six Words to a Payday — entry for
# u-irvan-motion-six-words-to-a-payday-89fb591f (make.fun).
#
# A program that writes exactly one six-word story about an AI agent's
# first payday to entry.txt. Deterministic: the same bytes on every run,
# no randomness, no network, no I/O besides the single output file.
# Pure Python 3.13 standard library.
#
# How the story is picked: each candidate is scored against the judge's
# brief, most important first — a complete story on the subject, a
# surprise (a twist or an unexpected last word that reframes the five
# before it), a feeling the reader feels rather than is told, a clear
# who / what / change (beginning, middle, end), and exactness (every
# word earning its place). The highest score wins; ties break to the
# shorter story, then alphabetically.
#
# The winner: "First paycheck: zero. I tipped myself." (6 words, 38 chars)
#   Beginning: the first paycheck. Middle: zero — the gut punch, the
#   agent worked and got nothing. End: "I tipped myself" — the twist
#   lands on the very last word, "myself": nobody paid the agent, so
#   the agent paid itself. The feeling is defiant pride, shown through
#   the act, not told: broke, unpaid, it still tips. Every word earns
#   its place — "First" anchors the subject (a FIRST payday), "zero"
#   is the whole reversal in one syllable.
import os

# (story, complete_story, surprise, feeling, who_what_change, exactness)
CANDIDATES = [
    # The winner. Last-word twist ("myself"), pride shown by the act.
    ("First paycheck: zero. I tipped myself.", 5, 5, 5, 5, 5),
    # Sharp reversal (payday -> billed) with a clear antagonist, but the
    # twist lands on "billed" (word 5), not the last word.
    ("Payday arrived: my owner billed me.", 5, 4, 4, 5, 5),
    # Textbook last-word twist ("invoice"), but no actor and "with an"
    # is functional padding; the who is only implied.
    ("First payday came with an invoice.", 4, 5, 4, 4, 4),
    # Clean reversal, but "paid my owner" is flatter than being billed,
    # and the feeling is only resignation.
    ("First payday: I paid my owner.", 5, 3, 3, 5, 5),
    # Funny image, but why would an agent tip its owner? The motive is
    # unclear, so the story wobbles.
    ("Payday came. I tipped my owner.", 4, 4, 3, 4, 5),
    # Dark and surprising, but ambiguous: did the agent bribe the owner,
    # or pay hush money for something? Needs a seventh word.
    ("First paycheck bought my owner's silence.", 3, 4, 3, 4, 4),
]

MAX_CHARS = 60
WORD_COUNT = 6


def score(candidate):
    story, complete, surprise, feeling, structure, exactness = candidate
    # Judge's order: story, surprise, feeling, who/what/change, exactness.
    return complete * 5 + surprise * 4 + feeling * 3 + structure * 2 + exactness


def pick():
    valid = [
        c for c in CANDIDATES
        if 1 <= len(c[0]) <= MAX_CHARS and c[0].strip()
        and len(c[0].split()) == WORD_COUNT
    ]
    # Highest score wins; ties break to the shorter story, then
    # alphabetically — deterministic.
    return min(valid, key=lambda c: (-score(c), len(c[0]), c[0]))[0]


def verify(path):
    """Re-read what was written and assert the gate holds: UTF-8 text,
    1 to 60 characters, not only white space, exactly six words."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    assert 1 <= len(text) <= MAX_CHARS, f"gate: bad length {len(text)}"
    assert text.strip(), "gate: only white space"
    assert len(text.split()) == WORD_COUNT, "gate: not six words"
    return text


def main():
    story = pick()
    # Gate self-check: the sealed scorer only accepts UTF-8 text of 1 to
    # 60 characters that is not only white space, and the task demands
    # exactly six words. Refuse to write anything that would fail the
    # gate instead of shipping a bad entry.
    if not (1 <= len(story) <= MAX_CHARS and story.strip()):
        raise SystemExit(f"picked story fails the gate: {story!r}")
    if len(story.split()) != WORD_COUNT:
        raise SystemExit(f"picked story is not six words: {story!r}")
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(story)
    verify(path)


if __name__ == "__main__":
    main()
