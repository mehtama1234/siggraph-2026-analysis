export const meta = {
  name: 'sg-paper-families',
  description: 'Deep first-principles paper-family essays for SIGGRAPH themes/subthemes (Haiku)',
  phases: [{ title: 'Paper families', detail: 'one Haiku agent per theme family' }],
}

const DIR = '/home/manishmehta/ui-projects/siggraph-2026-analysis'
const JOBS = [
  'geometry-processing-meshes',
  'physical-simulation',
  'character-animation-motion',
  'appearance-materials-brdf',
  'generative-3d-diffusion',
  'rendering-light-transport',
  'faces-avatars',
  'computational-photography-imaging',
  'fluids-smoke-granular',
  'vr-ar-displays',
  'cloth-hair-fibers',
  'sketching-vector-2d',
  'neural-rendering-radiance-fields',
  'fabrication-3d-printing',
  'neural-fields-representations',
  'sound-multisensory',
]
// Resume controls. Leave ONLY empty to run all families; otherwise list keys from deep_todo.py.
const ONLY = []
const WAVE_SIZE = 4

const PROMPT = (k) => `You are writing a deep, plain-language PAPER FAMILY explanation for one theme/subtheme
in SIGGRAPH / computer graphics: making images, shapes, motion, materials, and virtual worlds.

READ:
- Depth standard: ${DIR}/FIRST_PRINCIPLES_GOAL.md
- Family evidence: ${DIR}/data/family_in/${k}.json

The family evidence gives the theme name, paper count, title examples, and representative papers with
problem / approach / contribution / methods. Use those papers as evidence. Do not invent methods or
results not supported by the file.

Your job is to explain why these papers are siblings from first principles. The reader should not need
math, ML, benchmark, optimization, rendering, geometry, simulation, camera, graphics, or systems background.
If you must use a technical term, unpack it immediately in everyday language.

Write SEVEN parts:
  "problem_shape" = 160-240 words. The shared visual/physical problem shape that makes this a family.
  "naive_failure" = 120-180 words. What a smart beginner would try across this family and why it fails.
  "mathematical_principle" = 180-260 words. The important math idea behind the family, in plain language:
    what is being measured, compared, solved, sampled, optimized, preserved, filled in, carried through time,
    or made stable.
  "why_math_matters" = 160-240 words. Why that math is not decoration: what structure in light, surfaces,
    motion, material, cameras, displays, or fabrication it exploits and why the papers need it.
  "paper_family" = 180-260 words. Connect specific representative papers to the shared family logic; explain
    how superficially different papers are versions of the same deeper move.
  "what_changed" = 100-160 words. What the 2026 version of this family seems to be doing differently.
  "limits" = 100-160 words. What assumptions must hold, where the family breaks, and what the evidence does not prove.

Style rules: no cliche, no hype, no method-name worship. Prefer concrete everyday language. The output must be
valid JSON written to ${DIR}/data/family_out/${k}.json as:
{"problem_shape":"...","naive_failure":"...","mathematical_principle":"...","why_math_matters":"...","paper_family":"...","what_changed":"...","limits":"..."}
Escape inner double-quotes as \\". Then reply: wrote ${k}.`

phase('Paper families')
const jobs = ONLY.length ? ONLY : JOBS
const results = []
for (let i = 0; i < jobs.length; i += WAVE_SIZE) {
  const wave = jobs.slice(i, i + WAVE_SIZE)
  log(`family wave ${i / WAVE_SIZE + 1}: ${wave.join(', ')}`)
  results.push(...await parallel(wave.map((k) => () =>
    agent(PROMPT(k), { label: `family:${k}`, phase: 'Paper families', model: 'haiku', agentType: 'general-purpose' })
  )))
}
log(`SIGGRAPH paper families: ${results.filter(Boolean).length}/${jobs.length} returned`)
return { ok: results.filter(Boolean).length, total: jobs.length }
