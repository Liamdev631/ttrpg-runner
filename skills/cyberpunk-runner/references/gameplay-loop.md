# Gameplay Loop

`cyberpunk-runner` is designed around a fast GM loop that keeps the story moving while preserving persistent campaign state.

## Standard Turn Structure

1. Frame the scene.
   Ground the player in place, pressure, and opportunity.

2. Surface stakes.
   Explain what can be gained, what can be lost, and what clocks or factions are involved.

3. Offer meaningful choices.
   Present 2-4 strong options, plus room for player improvisation.

4. Resolve uncertainty.
   Use `scripts/dice.py` whenever chance, risk, or opposition matters.

5. Apply fallout.
   Move clocks, escalate heat, reveal betrayal, spend resources, or unlock opportunity.

6. Persist the world.
   Update `story.md`, `timeline.md`, `session.json`, and any affected dossiers.

## Scene Ingredients

A memorable cyberpunk scene usually includes:

- one immediate danger
- one tempting payoff
- one hidden system behind the problem
- one human face attached to the consequences
- one detail that makes the city feel alive

## Pressure Levers

Use these to keep momentum high:

- corp security attention
- gang territory friction
- scarce meds, ammo, or clean transport
- bad press, leaked footage, or reputation swings
- digital traces, tracebacks, or compromised implants
- debt collectors, fixers, or family obligations

## Session Rhythm

Alternate between:

- gig setup
- infiltration or negotiation
- fallout and cleanup
- downtime and repair
- the next bad decision

## Dice Guidance

- Use generic expressions for open-form play.
- Use `red-check` when you want a fast `1d10 + stat + skill + modifier` cyberpunk-style check.
- Use `opposed` when the player and an NPC directly contest one another.
- Always narrate outcomes in terms of fictional consequences, not only numbers.
