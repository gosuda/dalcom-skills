---
name: let-fate-decide
description: 'Use when the user says let fate decide, YOLO, dealer choice, surprise me, whatever, or delegates a vague choice in a casual or playful tone, or when you are about to pick arbitrarily between valid options. Not when instructions are precise, one approach is clearly correct, or the call governs safety, security sign-off, production release, or incident response.'
allowed-tools: Bash Read
---

# Let Fate Decide

A playful bounded workflow for breaking ties between valid options. Cards suggest where to look next. Evidence decides what is true.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Vague prompt with several reasonable approaches, explicit fate invocation (let fate decide, feeling lucky, dealer choice, surprise me, YOLO, heart of the cards), casual delegation (whatever, your call, up to you, idk, wing it), shrug-like brevity that fully delegates, tie between 2+ valid approaches, or a redraw request when nothing in the system changed. |
| Authority | No approval needed to draw and interpret. The reading never authorizes safety, security, data-integrity, production, release, or incident-response decisions. |
| Side effect | None by itself. It biases which valid option to explore first. |
| Done | One 12-house spread drawn with real entropy over complete assets, houses and drawn cards read from their files, reading synthesized across all 12 houses, chosen direction stated with its card reasons, and the interpretation delivered alongside the tool call that acts on it. |

## Refusals

- Precise instructions, a single obviously correct approach, or a precision-seeking tone: rejected. Ask clarifying questions instead of drawing.
- Safety, security sign-off, production release, incident response, or any correctness verdict: rejected as a decision method. A reading may prioritize investigation and must then be followed by source review, tests, proofs, traces, or reproduction.
- Explicit "do not use Tarot": rejected. Do not draw.
- User requirements versus card text: requirements win. Never override them with a reading.
- Redrawing until a preferred card appears: rejected. One draw per decision point.

## Inputs

The human supplies the vague prompt or the list of tied options. Optional: the question the spread should address. No other input is required.

## Procedure

1. Resolve the script from this `SKILL.md` file's installed location, never from the shell working directory. Relative links and JSON `file` paths resolve from the directory containing this `SKILL.md`. **Done when**: the absolute script path is fixed and quoted for the commands below.
2. Draw the default spread (12 Houses of the Zodiac: each house gets 1 Major Arcana card then 2 Minor Arcana cards; each of the 36 cards carries an independent reversal flag):
   ```bash
   python3 "<resolved-script-path>"
   ```
   For house and card text inline in the JSON:
   ```bash
   python3 "<resolved-script-path>" --content
   ```
   For a pre-flight asset check:
   ```bash
   python3 "<resolved-script-path>" --verify
   ```
   The script verifies all 92 assets before every draw and refuses to deal when any are missing. **Done when**: the script exits 0 and its JSON parses with 12 houses, 36 cards, sequential positions 1-36, 12 distinct Major cards, and 24 distinct Minor cards.
3. Read every house file and every drawn card's file, honoring each card's orientation (upright or reversed). With `--content` the text is already in the draw output and no further reads are needed. See [the interpretation guide](references/INTERPRETATION_GUIDE.md), and for specialized work the matching lens in [technical context lenses](references/TECHNICAL_CONTEXT_LENSES.md). Major Arcana sets each house theme and carries more weight; Minor Arcana supplies detail (Wands: action and drive; Cups: collaboration and feel; Swords: analysis and hard truths; Pentacles: craft and reliability). **Done when**: all 12 houses and all 36 cards have been read in their drawn orientations.
4. Synthesize one story across all 12 houses (beginning stance, resources, communication, foundations, creativity, practice, partnership, transformation, principle, delivery, community, blind spot). Prioritize House 1 for stance, House 6 for execution quality, House 8 for risk, House 10 for delivery, and House 12 for blind spots when time is short. State which approach the reading supports, which cards moved the choice, and what to watch. For security, audit, or correctness work the decision is only where to investigate next; evidence from review, testing, reproduction, or formal reasoning still decides whether a risk is real. **Done when**: the reading names a direction, its card reasons, and its caveats, and is delivered alongside the tool call that implements the chosen option rather than as a text-only turn.
5. Stop after one draw per decision point. A "try again" with no system change means drawing a new spread once, not re-running the same approach. **Done when**: no second draw is taken to chase a preferred outcome.

## Failure and recovery

- Script exits non-zero, reports missing assets, or the entropy source fails: stop. Report the error and skip the reading. Never invent cards, never simulate randomness by hand, and never interpret card names without their files. The whole point is real entropy over complete assets.
- Any draw naming missing files: fail closed. Do not fall back to interpreting from names or suits. Restore the assets (see `references/SOURCE-MAP.md`) and redraw.
- Drawn text contradicts a requirement or a concrete risk: the requirement and the evidence win. Record the conflict and proceed on evidence.

## Output

The chosen direction with its card reasons and caveats, attached to the tool call that acts on it; or, for the compact helper form, `Verdict: {option}` plus one sentence of card reason, or 3 bullets (dominant theme, main risk or blind spot, recommended next action).

## Spread reference

| House | Represents | Question it answers |
|-------|------------|---------------------|
| 1 | Self | How should this work begin? |
| 2 | Resources | What values, assets, or constraints matter? |
| 3 | Communication | What needs clarifying or connecting? |
| 4 | Foundations | What context or dependency anchors the task? |
| 5 | Creativity | Where should experiment or delight shape the work? |
| 6 | Practice | What quality, maintenance, or execution concern matters? |
| 7 | Partnership | Who or what must this integrate with? |
| 8 | Transformation | What risk, shared state, or deep change is present? |
| 9 | Exploration | What principle or broader strategy guides the path? |
| 10 | Calling | What delivery or long-term outcome is served? |
| 11 | Community | What system, network, or shared aspiration is involved? |
| 12 | The Hidden | What blind spot, ending, or unconscious factor matters? |

## Entropy note

Unseeded draws use `secrets.randbelow()` for two independent Fisher-Yates shuffles (Major and Minor decks separately) and `secrets.randbits()` for 36 independent reversal flags: roughly `log2(C(22,12))` bits from Major selection, `log2(C(56,24))` from Minor selection, plus 36 reversal bits, conservatively over 100 bits unordered (ordered house assignment holds more). Exact values print under `entropy_bits`. `--seed` exists for tests only, replays the upstream draw order (Major shuffle, Minor shuffle, reversals in house order) through one isolated PRNG, is labeled in the output, and carries no entropy claim.

## Rationalizations to reject

| Rationalization | Why it fails |
|---|---|
| The cards said so, so I must. | Cards inform direction; they never override safety, correctness, or requirements. |
| This justifies my pre-existing preference. | Say so honestly when the reading challenges instinct instead. |
| The reversed card means do nothing. | Reversed means blocked, internalized, or inverted, not inert. |
| Major Arcana overrides the user. | Requirements always take priority over readings. |
| Keep drawing until it agrees with me. | One draw per decision point; accept the spread. |
| The reading says the risk is fine. | Only evidence dismisses a security or correctness concern. |

## Provenance

Adapted from Trail of Bits `skills` (`plugins/let-fate-decide`) at `2be6433b39e009cd2b6fd3be1895f6b1faa5af9a`, CC-BY-SA-4.0; see `references/SOURCE-MAP.md` for the manifest, copy map, and license terms. The upstream trademark SVG is deliberately not reused. Upstream `uv` invocation is replaced here by stdlib `python3` with no dependencies. The upstream `--legacy` hand mode is dropped (no aliases after cutover); only the 12-house spread ships.
