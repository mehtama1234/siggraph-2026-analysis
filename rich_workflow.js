export const meta = {
  name: 'sg-deep-firstprinciples',
  description: 'Very deep first-principles no-jargon per-paper essays for SIGGRAPH/TOG 2026 (Haiku, 11 batches)',
  phases: [{ title: 'Deep writeups', detail: 'one Haiku agent per 15-paper batch' }],
}
const DIR = '/home/manishmehta/ui-projects/siggraph-2026-analysis'
const N = 11
// Resume controls. Leave ONLY empty to run everything; otherwise list batches like ['b000','b010'].
const ONLY = []
const WAVE_SIZE = 6

const PROMPT = (b) => `You are writing for a curious, smart reader who is NOT a computer-graphics specialist.
Read the batch file and produce a VERY DEEP, first-principles, plain-language explanation of EACH paper.
This is SIGGRAPH / ACM Transactions on Graphics — the field of making images, shapes, motion,
materials, and virtual worlds on a computer (rendering, geometry, simulation, animation, capture).

Batch file to READ: ${DIR}/data/batches/${b}.json
A JSON list of papers, each with: gid, title, abstract, theme.
Depth standard to READ and follow: ${DIR}/FIRST_PRINCIPLES_GOAL.md

For EACH paper write a real conceptual essay broken into ten named parts. Rules that matter more than anything:
- NO JARGON. If you must use a technical term, unpack it in plain words in the same breath.
  Banned unless immediately explained: "mesh", "manifold", "implicit field", "radiance",
  "latent", "diffusion prior", "differentiable", "parameterization", "SDF", "Gaussian",
  "topology", "regularization", "SOTA", "leverage", "novel", "framework", "paradigm".
  Prefer everyday words and physical intuition (light, surfaces, cloth, bouncing, folding).
- NO CLICHE, no hype. Say concrete things.
- FIRST PRINCIPLES: start from the real physical or visual object being modeled: light, surfaces,
  motion, material, geometry, camera measurement, user control, or simulation. Do not start from
  the method name.
- DEEP MECHANISM: explain the moving parts step by step, as if the reader had to rebuild the
  idea from scratch after reading your explanation.
- MATHEMATICAL CONCEPTS: name the actual mathematical ideas being used, but define each in
  plain language and explain why that mathematical move fits this paper.
- CONNECT THE DOTS: connect this paper to at least two neighboring SIGGRAPH ideas when the
  abstract supports it: geometry, light transport, optimization, simulation, time, random sampling,
  coordinate changes, surfaces, curves, diffusion/generation, reconstruction, animation, control.
- Ground every claim in THIS paper's abstract. Invent no numbers or methods not present.
- If the abstract is thin, say what can be inferred and what cannot. Do not fill gaps with generic filler.

The ten parts:
  "bp" = BIG PICTURE, 120-180 words. What visual/physical problem this serves and why anyone needs this paper before naming the method.
  "wh" = WHY IT IS HARD, 120-180 words. The central tension and why the obvious/simple approach breaks.
  "naive" = THE NAIVE SOLUTION, 90-140 words. What a smart beginner would try first, and exactly where it fails.
  "ap" = CORE IDEA, 120-180 words. The paper's central move in concrete, mechanical terms.
  "mech" = HOW THE MECHANISM RUNS, 180-260 words. Step-by-step: what goes in, what is transformed, what is compared/scored/optimized, what comes out.
  "math" = MATHEMATICAL CONCEPTS, 180-260 words. The mathematical objects and ideas being used, explained from first principles and tied to this paper.
  "dots" = CONNECTING THE DOTS, 120-180 words. How this paper relates to recurring SIGGRAPH ideas and why it sits in the broader field.
  "ww" = WHY IT WORKS, 140-220 words. The causal/intuitive reason the mechanism should improve over the naive approach.
  "po" = PAYOFF, 80-130 words. What capability/result it buys, grounded in the abstract.
  "limits" = LIMITS AND ASSUMPTIONS, 80-130 words. What must be true for this to work and what the abstract does not prove.

Write OUTPUT as JSON to this exact path: ${DIR}/data/rich_out/${b}.json
Object keyed by the paper's gid (string) -> {"bp":...,"wh":...,"naive":...,"ap":...,"mech":...,"math":...,"dots":...,"ww":...,"po":...,"limits":...}.
IMPORTANT: escape any double-quote inside a value as \\" so the JSON parses. Include every paper.
Then reply with just: wrote ${b} (COUNT papers).`

phase('Deep writeups')
const items = ONLY.length ? ONLY : Array.from({ length: N }, (_, i) => `b${String(i).padStart(3, '0')}`)
const results = []
for (let i = 0; i < items.length; i += WAVE_SIZE) {
  const wave = items.slice(i, i + WAVE_SIZE)
  log(`SIGGRAPH deep wave ${i / WAVE_SIZE + 1}: ${wave.join(', ')}`)
  results.push(...await parallel(wave.map((b) => () =>
    agent(PROMPT(b), { label: `sg-deep:${b}`, phase: 'Deep writeups', model: 'haiku', agentType: 'general-purpose' })
  )))
}
log(`SIGGRAPH deep pass: ${results.filter(Boolean).length}/${items.length} returned`)
return { ok: results.filter(Boolean).length, total: items.length }
