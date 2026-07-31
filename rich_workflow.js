export const meta = {
  name: 'sg-rich-firstprinciples',
  description: 'Rich first-principles no-jargon per-paper writeups for SIGGRAPH/TOG 2026 (Haiku, 11 batches)',
  phases: [{ title: 'Rich writeups', detail: 'one Haiku agent per 15-paper batch' }],
}
const DIR = '/home/manishmehta/ui-projects/siggraph-2026-analysis'
const N = 11

const PROMPT = (b) => `You are writing for a curious, smart reader who is NOT a computer-graphics specialist.
Read the batch file and produce a RICH, first-principles, plain-language explanation of EACH paper.
This is SIGGRAPH / ACM Transactions on Graphics — the field of making images, shapes, motion,
materials, and virtual worlds on a computer (rendering, geometry, simulation, animation, capture).

Batch file to READ: ${DIR}/data/batches/${b}.json
A JSON list of papers, each with: gid, title, abstract, theme.

For EACH paper write five short parts. Rules that matter more than anything:
- NO JARGON. If you must use a technical term, unpack it in plain words in the same breath.
  Banned unless immediately explained: "mesh", "manifold", "implicit field", "radiance",
  "latent", "diffusion prior", "differentiable", "parameterization", "SDF", "Gaussian",
  "topology", "regularization", "SOTA", "leverage", "novel", "framework", "paradigm".
  Prefer everyday words and physical intuition (light, surfaces, cloth, bouncing, folding).
- NO CLICHE, no hype. Say concrete things.
- FIRST PRINCIPLES: explain the *why* and the mechanism, not just what was done.
- CONNECT THE DOTS: part 1 zooms OUT to the real thing we ultimately want (a believable image,
  a shape that behaves like the real object, a character that moves right) so a newcomer sees
  why the paper exists.
- Ground every claim in THIS paper's abstract. Invent no numbers or methods not present.

Five parts (each 2-4 sentences, plain prose, no lists inside):
  "bp" = THE BIG PICTURE: the real-world goal this serves and why it matters. Zoom out.
  "wh" = WHY IT'S HARD: the specific tension — why the obvious approach fails here.
  "ap" = WHAT THEY DO: the actual idea/mechanism, in plain terms a newcomer can picture.
  "ww" = WHY IT WORKS: the first-principles reason the mechanism actually helps — the intuition.
  "po" = THE PAYOFF: what it concretely buys, grounded in the abstract.

Write OUTPUT as JSON to this exact path: ${DIR}/data/rich_out/${b}.json
Object keyed by the paper's gid (string) -> {"bp":...,"wh":...,"ap":...,"ww":...,"po":...}.
IMPORTANT: escape any double-quote inside a value as \\" so the JSON parses. Include every paper.
Then reply with just: wrote ${b} (COUNT papers).`

phase('Rich writeups')
const items = Array.from({ length: N }, (_, i) => `b${String(i).padStart(3, '0')}`)
const results = await parallel(items.map((b) => () =>
  agent(PROMPT(b), { label: `sg-rich:${b}`, phase: 'Rich writeups', model: 'haiku', agentType: 'general-purpose' })
))
log(`SIGGRAPH rich pass: ${results.filter(Boolean).length}/${N} returned`)
return { ok: results.filter(Boolean).length, total: N }
