export const meta = {
  name: 'sg-deep-concepts',
  description: 'Deep first-principles conceptual essays for recurring math ideas and paper families of graphics (Haiku)',
  phases: [{ title: 'Concept essays', detail: 'one Haiku agent per math concept / paper family' }],
}
const DIR = '/home/manishmehta/ui-projects/siggraph-2026-analysis'
const KEYS = ['modes','curve','integrate','random','time','optimize','solve','connect']
// Resume controls. Leave ONLY empty to run all concepts; otherwise list keys like ['curve','time'].
const ONLY = []
const WAVE_SIZE = 4

const PROMPT = (k) => `You are writing the definitive plain-language, first-principles explanation of ONE recurring
mathematical idea that shows up across computer-graphics research (SIGGRAPH / ACM Transactions on
Graphics — making images, shapes, motion, materials, and virtual worlds on a computer).

READ this file: ${DIR}/data/concept_in/${k}.json
Also read the depth standard: ${DIR}/FIRST_PRINCIPLES_GOAL.md
It has: key, title, intro + why (a short earlier draft — you must go DEEPER and RICHER than these),
n_total (how many papers lean on this idea), and papers[] (real papers under it, each with a
plain 'uses' note). The papers are your evidence for connecting the dots.

Write SIX parts. Rules that matter more than anything:
- NO JARGON. If a technical term is unavoidable, unpack it in plain words in the same breath.
  Prefer everyday words and physical intuition (light, cloth, water, folding, bouncing) over
  named techniques.
- NO CLICHE, no hype. Every sentence must carry a real idea.
- FIRST PRINCIPLES: build the idea up from scratch — what problem in making pictures/shapes/motion
  would force a thoughtful person to INVENT this? Assume the reader has not seen it before.
- PAPER FAMILY: explain why these papers belong together as siblings, not merely because they share a tag.
- MATHEMATICAL IMPORTANCE: do not just name the concept. Explain what need it answers, what it measures
  or preserves, what assumption makes it useful, and where that assumption breaks.
- CONNECT THE DOTS: draw on the ACTUAL papers[] in the file — show how this one idea wears many
  disguises across them, so the reader sees the single thread under many different papers.
- Go deeper than the provided intro/why; treat those only as a floor you must exceed.

The six parts:
  "idea"    = THE IDEA, FROM SCRATCH: the real need in graphics that forces this idea into existence,
              and what the idea actually IS once you strip away all notation. 8-12 sentences.
  "why"     = WHY IT WORKS: the underlying reason/guarantee that makes it valid — the actual
              mechanism of why it works and where it breaks. 7-10 sentences.
  "math"    = THE MATHEMATICAL PRINCIPLE: the important mathematical object or move, explained without
              prior math knowledge. Say what is being measured, compared, optimized, solved, sampled,
              preserved, filled in, or carried through time, and why that matters. 8-12 sentences.
  "family"  = THE PAPER FAMILY: why these papers are siblings; the shared problem shape, repeated
              failure mode, and common mathematical move across the family. 7-10 sentences.
  "dots"    = CONNECTING THE DOTS: how this single idea recurs across the specific papers in this
              group — the shared move under superficially different problems. Ground it in papers[].
              8-12 sentences.
  "picture" = ONE concrete everyday analogy that makes the idea click. 2-3 sentences.

Write OUTPUT as JSON to this exact path: ${DIR}/data/concept_out/${k}.json
A single object: {"idea":"...","why":"...","math":"...","family":"...","dots":"...","picture":"..."}.
Escape any double-quote inside a value as \\" so the JSON parses. Then reply: wrote ${k}.`

phase('Concept essays')
const jobs = ONLY.length ? ONLY : KEYS
const results = []
for (let i = 0; i < jobs.length; i += WAVE_SIZE) {
  const wave = jobs.slice(i, i + WAVE_SIZE)
  log(`concept wave ${i / WAVE_SIZE + 1}: ${wave.join(', ')}`)
  results.push(...await parallel(wave.map((k) => () =>
    agent(PROMPT(k), { label: `concept:${k}`, phase: 'Concept essays', model: 'haiku', agentType: 'general-purpose' })
  )))
}
log(`SIGGRAPH concept essays: ${results.filter(Boolean).length}/${jobs.length} returned`)
return { ok: results.filter(Boolean).length, total: jobs.length }
