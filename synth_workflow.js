export const meta = {
  name: 'math-synthesis',
  description: 'One-page synthesis tying the recurring math ideas into a single narrative (Haiku)',
  phases: [{ title: 'Synthesis', detail: 'one agent per conference' }],
}

const JOBS = [
  { dir: '/home/manishmehta/ui-projects/data-mining-conferences-2026',
    field: 'data mining / the web / information retrieval / recommendation',
    goal: 'connecting a person to the right, trustworthy answer out of a world too vast to read' },
  { dir: '/home/manishmehta/ui-projects/siggraph-2026-analysis',
    field: 'computer graphics (making images, shapes, motion, materials, and virtual worlds)',
    goal: 'turning math into a believable picture, shape, or motion' },
]

const PROMPT = (j) => `You are writing THE OPENING of a page called "The mathematics of ${j.field}, from first principles."
Below the opening will sit ~8-11 sections, each explaining ONE recurring mathematical idea in depth.
Your job: the single-page SYNTHESIS that ties them all together into ONE story, so a newcomer sees the
whole field as a few connected ideas rather than a pile of techniques.

READ this file: ${j.dir}/data/synth_in.json — it has concepts[], each with title, n_papers, and the
already-written rich essay parts (idea / why / dots). These ARE the sections. Read them all, then rise above.

Write THREE parts. Rules that matter most:
- NO JARGON (unpack any unavoidable term in plain words). NO CLICHE. Every sentence carries a real idea.
- FIRST PRINCIPLES and BIG PICTURE: the reader should finish feeling they understand the SHAPE of the
  whole field's mathematics, not a list.
- CONNECT THE DOTS: do not just summarize each idea — show how they DEPEND ON and FEED each other, in a
  natural order (what has to happen first, what builds on what). Name the ideas by their plain titles.
- Ground it: the overarching real-world goal of this field is roughly "${j.goal}". Tie the math back to that.

The three parts:
  "thread" = THE ONE THREAD: the single big-picture problem all this mathematics ultimately serves, stated
             so a newcomer feels the stakes. 3-5 sentences.
  "arc"    = HOW THE IDEAS FIT: walk the reader through the handful of ideas AS ONE CONNECTED ARC — this
             idea turns X into something you can work with, which lets the next idea do Y, which the next
             then Z. Name them by title; show the dependencies. 8-12 sentences.
  "punchline" = THE PUNCHLINE: the deep takeaway — what the whole toolkit really is, and (if true) how the
             newer learning-from-examples layer sits ON TOP of the older, simpler ideas rather than
             replacing them. 3-5 sentences.

Write OUTPUT as JSON to: ${j.dir}/data/synth_out.json
A single object {"thread":"...","arc":"...","punchline":"..."}. Escape inner double-quotes as \\".
Then reply: wrote synthesis (${j.field}).`

phase('Synthesis')
const results = await parallel(JOBS.map((j) => () =>
  agent(PROMPT(j), { label: `synth:${j.dir.split('/').pop()}`, phase: 'Synthesis', model: 'haiku', agentType: 'general-purpose' })
))
log(`synthesis: ${results.filter(Boolean).length}/${JOBS.length} returned`)
return { ok: results.filter(Boolean).length }
