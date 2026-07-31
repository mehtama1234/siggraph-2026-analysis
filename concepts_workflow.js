export const meta = {
  name: 'sg-rich-concepts',
  description: 'Rich first-principles conceptual essays for the recurring math ideas of graphics (Haiku)',
  phases: [{ title: 'Concept essays', detail: 'one Haiku agent per math concept' }],
}
const DIR = '/home/manishmehta/ui-projects/siggraph-2026-analysis'
const KEYS = ['modes','curve','integrate','random','time','optimize','solve','connect']

const PROMPT = (k) => `You are writing the definitive plain-language, first-principles explanation of ONE recurring
mathematical idea that shows up across computer-graphics research (SIGGRAPH / ACM Transactions on
Graphics — making images, shapes, motion, materials, and virtual worlds on a computer).

READ this file: ${DIR}/data/concept_in/${k}.json
It has: key, title, intro + why (a short earlier draft — you must go DEEPER and RICHER than these),
n_total (how many papers lean on this idea), and papers[] (real papers under it, each with a
plain 'uses' note). The papers are your evidence for connecting the dots.

Write FOUR parts. Rules that matter more than anything:
- NO JARGON. If a technical term is unavoidable, unpack it in plain words in the same breath.
  Prefer everyday words and physical intuition (light, cloth, water, folding, bouncing) over
  named techniques.
- NO CLICHE, no hype. Every sentence must carry a real idea.
- FIRST PRINCIPLES: build the idea up from scratch — what problem in making pictures/shapes/motion
  would force a thoughtful person to INVENT this? Assume the reader has not seen it before.
- CONNECT THE DOTS: part 3 must draw on the ACTUAL papers[] in the file — show how this one idea
  wears many disguises across them, so the reader sees the single thread under many different papers.
- Go deeper than the provided intro/why; treat those only as a floor you must exceed.

The four parts:
  "idea"    = THE IDEA, FROM SCRATCH: the real need in graphics that forces this idea into existence,
              and what the idea actually IS once you strip away all notation. 5-8 sentences.
  "why"     = WHY IT WORKS: the underlying reason/guarantee that makes it valid — the actual
              mechanism of why it works (and where it breaks). 4-6 sentences.
  "dots"    = CONNECTING THE DOTS: how this single idea recurs across the specific papers in this
              group — the shared move under superficially different problems. Ground it in papers[].
              5-8 sentences.
  "picture" = ONE concrete everyday analogy that makes the idea click. 2-3 sentences.

Write OUTPUT as JSON to this exact path: ${DIR}/data/concept_out/${k}.json
A single object: {"idea":"...","why":"...","dots":"...","picture":"..."}.
Escape any double-quote inside a value as \\" so the JSON parses. Then reply: wrote ${k}.`

phase('Concept essays')
const results = await parallel(KEYS.map((k) => () =>
  agent(PROMPT(k), { label: `concept:${k}`, phase: 'Concept essays', model: 'haiku', agentType: 'general-purpose' })
))
log(`SIGGRAPH concept essays: ${results.filter(Boolean).length}/${KEYS.length} returned`)
return { ok: results.filter(Boolean).length, total: KEYS.length }
