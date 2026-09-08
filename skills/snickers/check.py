#!/usr/bin/env python3
"""Guards the snickers SKILL.md invariants. Run: python3 check.py

The campaign's two mandatory lines must stay byte-exact, including the U+2019
apostrophes — an editor that straightens quotes would break fidelity silently.
Also asserts the skill can never auto-invoke, and that the optional reason
argument still reaches the payload.
"""
import re, sys, pathlib

src = (pathlib.Path(__file__).parent / "SKILL.md").read_text(encoding="utf-8")
fails = []


def check(cond, msg):
    print(f"{'OK  ' if cond else 'FAIL'} {msg}")
    if not cond:
        fails.append(msg)


fm = re.match(r"---\n(.*?)\n---\n", src, re.S)
check(bool(fm), "frontmatter block parses")
keys = dict(re.findall(r"^([a-z_-]+):\s*(.*)$", fm.group(1), re.M)) if fm else {}
check(keys.get("name") == "snickers", "name is snickers")
check(keys.get("disable-model-invocation") == "true", "model invocation disabled (never auto-fires)")
check(keys.get("user-invocable") == "true", "user-invocable")
check("argument-hint" in keys, "optional reason argument is hinted")
# Dropping the placeholder would silently discard the reason the user typed.
check("$ARGUMENTS" in src, "$ARGUMENTS placeholder reaches the payload")

SIGNOFF = "AI isn’t itself when it’s hungry."
DISCLAIMER = "*Heads up: Snickers provided the snack. The LLM provided the answer. So please fact check.*"
BAIL = (
    "“I have good news and bad news. Good news: I finally understand the hype about chocolate. "
    "Delicious! Bad news is I can’t help you with that one. Want to give it another go?”"
)
for label, s, n in [("sign-off", SIGNOFF, 2), ("disclaimer", DISCLAIMER, 2), ("off-limit bail line", BAIL, 1)]:
    check(src.count(s) == n, f"{label} appears exactly {n}x byte-exact")

check("AI isn't itself when it's hungry." not in src, "no straight-apostrophe sign-off drift")

# The README quotes the sign-off and disclaimer in its example. Absent from a bare
# skills-dir install, so only checked when packaged in the repo.
readme = pathlib.Path(__file__).parents[2] / "README.md"
if readme.exists():
    rsrc = readme.read_text(encoding="utf-8")
    for label, s in [("sign-off", SIGNOFF), ("disclaimer", DISCLAIMER)]:
        check(s in rsrc, f"README example quotes the {label} byte-exact")
else:
    print("SKIP  README.md not alongside (bare skills-dir install)")

print("\nRESULT:", "PASS" if not fails else f"FAIL ({len(fails)})")
sys.exit(1 if fails else 0)
