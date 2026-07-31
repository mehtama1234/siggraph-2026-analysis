# Deep First-Principles Analysis Goal

Build the site as a deeply explanatory map of the conference, not a collection of paper summaries. The goal is not to make the explanations longer. The goal is to make them structurally deeper: every page should teach the reader how to think about the problem from the ground up, why the mathematical idea had to appear, and how separate papers are different attempts to solve the same underlying difficulty.

The reader is smart and curious, but should not need prior knowledge of math, machine learning jargon, benchmark jargon, optimization jargon, rendering jargon, geometry jargon, simulation jargon, camera jargon, graphics jargon, or systems jargon. Every technical idea must be rebuilt from ordinary language before it is named.

## What The Analysis Must Teach

For every paper, theme, subtheme, mathematical concept, and paper family, explain:

- the real-world visual or physical thing being made, measured, reconstructed, animated, simulated, generated, displayed, or fabricated
- why the problem exists before any method is introduced
- what a smart beginner would try first
- exactly why that naive attempt fails
- the paper's central move in concrete mechanical terms
- what goes in, what gets transformed, what is compared or solved, and what comes out
- the mathematical principle underneath the method, explained without assuming notation
- why that mathematical principle fits the problem
- what structure in the physical or visual world the math is exploiting
- how this paper connects to sibling papers, neighboring subthemes, and the broader field
- what assumptions must hold, and what the abstract does not prove

The explanation is incomplete if it only says what the authors did. It must also explain why the problem is naturally difficult before the method exists, why simpler ideas fail, and why the chosen mathematical structure is a good fit.

## Per-Paper Standard

Each paper should read like a small conceptual lesson. It should not simply restate the abstract. The explanation should start from the underlying object: light moving through a scene, a surface bending, a shape being stored, a body moving through time, a camera capturing incomplete evidence, a material answering light, a display trying to fool the eye, or a design becoming a physical object.

For each paper, the reader should be able to answer these questions after reading:

- What ordinary visual, physical, or design problem is this paper trying to handle?
- What would someone naturally try first?
- What exactly breaks in that simple attempt?
- What information does the paper measure, store, move, smooth, sample, solve, render, reconstruct, or generate?
- What mathematical idea makes that move possible?
- Why is that math a better language for the problem than a hand-written rule?
- What sibling papers are solving the same deeper problem with a different surface vocabulary?
- What must be true about the scene, material, body, camera, display, or data for the claim to be trustworthy?

The paper-level story should include:

- `bp`: big picture
- `wh`: why it is hard
- `naive`: the naive solution and why it fails
- `ap`: the core idea
- `mech`: how the mechanism runs step by step
- `math`: the mathematical concepts being used
- `dots`: how it connects to themes, subthemes, and paper families
- `ww`: why it works
- `po`: payoff
- `limits`: limits and assumptions

Minimum depth: each field should contain a real explanation, not a label. The `math`, `mech`, `dots`, and `limits` fields are the main anti-shallow fields. They should name the moving parts, describe how they interact, and avoid merely repeating method names from the abstract.

## Theme, Subtheme, And Paper-Family Standard

A theme or family should answer: why do these papers belong together?

For each family, explain the shared problem shape, the repeated failure mode, the recurring mathematical tools, and what changed in 2026. The family explanation should make the reader see that superficially different papers are often solving the same deeper problem: measuring shape, following time, adding many small contributions, solving many constraints at once, sampling what matters, filling gaps between known measurements, changing coordinates without breaking relationships, or learning a rule from examples.

Themes and subthemes must not be umbrella labels. They should act like connective tissue across papers. A good family explanation says:

- Here is the common real-world pressure that keeps appearing.
- Here is the naive strategy that many papers are trying to move beyond.
- Here is the recurring mathematical move.
- Here is why that move appears in many different-looking papers.
- Here are the papers that represent different branches of the same idea.
- Here is what changed this year: speed, fidelity, control, editability, physical plausibility, data scarcity, capture difficulty, display limits, or fabrication constraints.

When explaining a family, avoid listing papers one by one. Instead, organize the family around the hidden shared problem. For example, rendering, materials, and neural appearance papers often look different on the surface, but many are really about adding up how light arrives while avoiding impossible computation. Geometry, fabrication, and simulation papers often ask how to change a shape while preserving the relationships that make it usable. Animation and motion papers often ask how to make time obey both intent and physical constraints.

## Math Standard

Do not say "uses optimization" and stop. Explain what is being adjusted: shape, motion, lighting, material, camera placement, display behavior, or model settings. Explain what counts as wrong and why reducing that wrongness makes the result more believable.

Do not say "uses integration" and stop. Explain what many tiny pieces are being added up: light paths, forces, mass, area, volume, or time steps.

Do not say "uses geometry" and stop. Explain what has to stay true about the shape: distance, angle, curvature, connection, inside/outside, smoothness, or contact.

Every mathematical concept must answer three questions:

- What problem forced this idea into existence?
- What is the idea in everyday language?
- Why does this idea work for this family of papers?

Also explain the shape of the mathematical object in plain language:

- If the paper adds many tiny effects, explain what pieces are being added and why no single piece is enough.
- If the paper solves constraints, explain what must be true at the same time and what has to bend when the constraints conflict.
- If the paper samples, explain why trying everything is impossible and what makes a sample worth spending computation on.
- If the paper stores a shape, explain what is kept, what is thrown away, and how the original surface can be recovered.
- If the paper follows time, explain what state changes from one moment to the next and what must remain consistent.
- If the paper uses learning, explain what pattern is being reused from examples and why reuse may fail outside those examples.
- If the paper changes coordinates, explain what becomes simpler after the change and what relationships must survive the change.
- If the paper uses physical laws, explain what quantity is conserved, balanced, minimized, or constrained.

The important concept behind a mathematical principle is usually a tradeoff. Name the tradeoff explicitly: detail versus speed, physical truth versus artistic control, smoothness versus sharp features, stability versus responsiveness, compact storage versus reconstruction quality, realism versus editability, local shape versus whole-object consistency, or exact simulation versus useful approximation.

## Rejection Criteria

Reject and regenerate any output that does these things:

- defines the paper only by its method name
- says "more realistic" without explaining what visual or physical failure is reduced
- says "uses optimization/integration/geometry/simulation/rendering" without rebuilding the idea in everyday language
- lists papers without explaining the shared problem underneath them
- explains an evaluation result but not the real-world task the evaluation is standing in for
- uses jargon as a shortcut instead of translating it
- gives a payoff without limits or assumptions
- sounds like a generic abstract that could fit many papers

## Style

Use plain, concrete language. Avoid cliches, hype, and method-name worship. Banned unless unpacked immediately: mesh, manifold, implicit field, radiance, latent, diffusion prior, differentiable, parameterization, SDF, Gaussian, topology, regularization, SOTA, benchmark, ablation, robust, framework, paradigm, leverage, optimization, simulation, rasterization.

Prefer everyday explanations: light bouncing, cloth folding, water flowing, a surface bending, a camera missing information, a shape being stored compactly, a body moving through time, a display working around the eye, a printer obeying physical limits, filling gaps from nearby evidence, and checking what must be true for the answer to be trusted.
