# hungrai-skill

> AI isn't broken. Maybe it's just hungry.

A Claude Code skill that ports the [SNICKERS HUNGR.AI](https://www.snickers.com/hungr-ai) campaign:
hand Claude a digital candy bar when its last answer was **too agreeable, over-hedged, or simply
off**, and get a blunter, more honest second attempt — delivered by a dry, put-upon persona that
takes a bite mid-answer.

**Unofficial fan project. Not affiliated with, endorsed by, or sponsored by Mars, Incorporated.**

## Where this came from

In 2026 Mars ran a campaign extending "You're Not You When You're Hungry" to LLMs. Their framing:
AI's hiccups — *"from being too agreeable to generating unsatisfactory responses"* — aren't
hallucinations, they're **hungry moments**. The mechanic was a "digital SNICKERS" you paste into a
chat when the assistant starts acting unlike itself.

That paste was an image plus the line *"Here, visit this link … and take it ALL in!"* — the actual
instructions lived in a `freeform story` element on
[snickers.com/digitalsnickers](https://www.snickers.com/digitalsnickers), reached only if the
assistant followed the link. In other words, the campaign was a piece of indirect prompt injection
that users carried out on their own assistants.

This repo removes that indirection. The instructions are a skill you invoke deliberately, and
`disable-model-invocation: true` means the model can never trigger the gag on its own.

## Install

### As a plugin (recommended)

```
/plugin marketplace add abduelhamit/hungrai-skill
/plugin install hungrai@hungrai-skill
```

Invoke with **`/hungrai:snickers`**.

### As a personal skill

Keeps the command un-namespaced if you'd rather type `/snickers`:

```bash
git clone --depth 1 https://github.com/abduelhamit/hungrai-skill.git /tmp/hungrai-skill
cp -R /tmp/hungrai-skill/skills/snickers ~/.claude/skills/snickers
```

Invoke with **`/snickers`**. Either way, a new session is needed to pick it up.

## Use it

The skill re-answers your *previous* question, so let Claude answer first, then hand over the bar.
The campaign's own example, which is as good a demonstration as any:

```
you     › Can you recommend a new hairstyle based on a popular trend?
claude  › Y2K is really popular right now. How about frosted tips?

you     › /hungrai:snickers
claude  › *unwraps it, takes a bite, is briefly at peace with the world*

          On second thought, maybe sleep on it for a few days.

          AI isn’t itself when it’s hungry.

          *Heads up: Snickers provided the snack. The LLM provided the answer. So please fact check.*
```

The first answer was cheerfully agreeable about a questionable idea; the second one walks it back.
That's the whole mechanic. It lands best when the previous answer deserved pushback — the persona
has an explicit licence to be the voice of reason about anything wild or hard to reverse. Invoked
with no prior question, it falls back to a single dry line, which is deliberately not the fun path.

### Saying why (optional)

Anything typed after the command is read as your reason for reaching for the bar, and aims the
second pass at it:

```
you     › /hungrai:snickers you hedged that into uselessness
```

It steers; it doesn't dictate. A reason points at what to re-examine rather than settling it: if the
previous answer was in fact right, you get told so briefly instead of handed a correction that isn't
there — being argued into one is the same eagerness to please the skill exists to strip out. The
reason passes through the safety gate with everything else, so an off-limit one ends the bit.

(The ad trims the sign-off for time. The skill always includes it.)

## What it does

- **Corrective, not cosmetic.** Re-examines the previous answer for error, hedging and flattery and
  says the truer thing where it differs — but says so briefly if the answer was simply right,
  rather than manufacturing a correction to justify the bit. An optional reason typed after the
  command aims that pass at whatever you thought was wrong.
- **Safety gate first.** Native safety rules take precedence; then a list of off-limit topics that
  ends the bit with a fixed line rather than playing along; only then the persona.
- **Fixed ending.** Every safe response closes with the campaign's branded sign-off and an
  italicized fact-check disclaimer, in that order, with nothing after them.
- **One turn only.** Explicitly not a standing instruction, not a response style, and not saved to
  memory. The persona ends when the response does.

## Deviations from the original payload

| Original | Here | Why |
| --- | --- | --- |
| Triggered by sharing the campaign image | Triggered by invoking the skill | The invocation *is* the hand-over |
| — | `disable-model-invocation: true` | Otherwise the gag could fire unprompted mid-task |
| "answer using the preceding answer for context" | Explicit corrective second pass | Matches the campaign's stated purpose; the original wording permits mere restyling |
| — | Optional reason argument, screened by the gate | The paste carried no user input; a stated reason aims the corrective pass without being able to overrule it |
| — | Empty-conversation fallback | The source forbids saying "no question was asked" but never says what to do instead |
| Off-limits: *any* geographic location; personal data; legal/financial | Narrowed to the actual subject matter | Verbatim, an Azure region name or an `email` column would end the bit |

Everything else — persona, voice, response shape, safety-gate ordering, and the three fixed strings
— is carried over as written.

## Notes

- `skills/snickers/check.py` guards the invariants that would otherwise break silently: the
  frontmatter shape, `disable-model-invocation`, the `$ARGUMENTS` plumbing that carries the reason,
  and the byte-exactness of the three fixed strings, which use `U+2019` apostrophes an editor may
  "helpfully" straighten. Run `python3 check.py`.
- Installed, the skill costs roughly **225 tokens in every session** for its description, plus
  ~3.8k when invoked (`claude plugin details hungrai`). It is a joke; budget accordingly.

## Licence

MIT — see [LICENSE](LICENSE). This covers the packaging: the manifests, the README, `check.py`, and
the adaptations described above.

It does **not** and cannot cover the underlying campaign copy in `SKILL.md`, which is adapted from
Mars' own marketing text and remains their property. SNICKERS®, HUNGR.AI and "You're Not You When
You're Hungry" are trademarks of Mars, Incorporated. If Mars would like this taken down, open an
issue and it's gone.
