# Production Demo Strategy

The current `source-code/` lab is a first-principles teaching layer. It proves
concepts visually. A client-ready demo layer needs a stricter goal:

> Given a client with a similar graphics, simulation, capture, optimization, or
> rendering problem, we should be able to open a focused demo, load representative
> input, change meaningful parameters, show measurable output, and reuse the code
> as a starter implementation.

That means the demos must move from toy sketches to reusable reference modules.

## What Production Grade Means Here

A production-grade demo is not a full product and not a full paper
reimplementation. It is a clean vertical slice:

- real input shape: image, mesh, point cloud, texture, camera pose, motion clip,
  material grid, or particle state
- reusable core module: pure functions/classes with typed inputs and outputs
- visible client workflow: upload/select input, run method, compare before/after
- measurable result: loss, smoothness, stretch, coverage, frame time, error,
  stability, memory, or quality proxy
- documented tradeoff: what improves, what gets worse, and when it fails
- export path: download output image/data/config or copy integration snippet
- tests: deterministic fixtures for the core math, not only visual inspection
- licensing boundary: toy/original code stays ours; author code is linked or
  wrapped only when license allows it

## Folder Standard

Each reusable demo should live in a self-contained subtheme folder:

```text
source-code/themes/<theme>/<subtheme>/
  README.md
  demo-spec.json
  src/
    core.js
    render.js
    fixtures.js
  tests/
    core.test.js
  examples/
    default-config.json
    sample-input.json
  author-code.md
```

The browser lab can import these modules, but the algorithm should not be trapped
inside the page. A client-facing engineer should be able to reuse `src/core.js`
without carrying the whole site UI.

## Demo Spec

Every production demo gets a `demo-spec.json`:

```json
{
  "id": "laplacian-smoothing",
  "theme": "Geometry Processing & Meshes",
  "subtheme": "Mesh denoising and fairing",
  "client_problem": "Clean scanned or generated geometry without erasing the object's silhouette.",
  "paper_family_claim": "Geometry papers preserve local shape relationships while removing noise or reducing cost.",
  "inputs": ["mesh vertices", "mesh edges", "locked boundary vertices"],
  "outputs": ["smoothed vertices", "roughness score", "area or volume change"],
  "core_algorithm": "neighbor averaging with constraint preservation",
  "demo_proves": "Local averaging removes high-frequency noise, but unconstrained smoothing shrinks the asset.",
  "failure_modes": ["thin features collapse", "boundaries drift", "important sharp edges blur"],
  "reuse_level": "starter-module",
  "license": "original"
}
```

## Ten Client-Ready Demo Targets

### 1. Mesh Cleanup For Scans Or Generated 3D

Current teaching demo: Laplacian smoothing.

Production version:

- load a small OBJ-like mesh fixture or generated noisy grid
- mark boundary/feature vertices as locked
- run smoothing, optional Taubin-style shrink compensation
- show before/after mesh, roughness, area change, max vertex movement
- export cleaned vertices

Client use:

- scanned assets
- generated 3D cleanup
- mesh repair pre-processing
- CAD visualization cleanup

Reusable core:

```text
smoothMesh(vertices, edges, options) -> { vertices, metrics }
```

### 2. SDF Shape Operations For Procedural Geometry

Current teaching demo: union/intersection/subtraction over distance fields.

Production version:

- compose primitive shapes with a node graph
- sample field to contour image or mesh preview
- expose boolean operations and smoothing radius
- export field config

Client use:

- procedural asset generation
- collision proxy construction
- product configurators
- implicit geometry prototyping

Reusable core:

```text
evaluateSdf(point, scene) -> signedDistance
sampleSdfGrid(scene, bounds, resolution) -> grid
```

### 3. Ray-Marched Inspection Renderer

Current teaching demo: sphere ray marching.

Production version:

- render any SDF scene from demo 2
- expose camera, light, shadow quality, max steps
- report frame time, hit rate, average steps, missed rays
- export PNG

Client use:

- fast implicit-shape preview
- engineering geometry inspection
- procedural modeling UI

Reusable core:

```text
rayMarch(camera, sdfScene, renderOptions) -> imageData + metrics
```

### 4. Differentiable Image Fitting

Current teaching demo: fit a soft circle to a target.

Production version:

- target can be drawn, loaded, or selected from fixtures
- optimize position, scale, color, and blur
- show loss curve and parameter trace
- pause/resume and export fitted parameters

Client use:

- inverse rendering starter
- camera/material/light calibration explainer
- visual parameter fitting for inspection systems

Reusable core:

```text
fitParameters(targetImage, renderer, params, options) -> { params, lossHistory }
```

### 5. Gaussian Splat Previewer

Current teaching demo: soft colored blobs.

Production version:

- load a small splat JSON fixture
- sort by depth, blend by alpha, cull outside camera
- expose splat radius, opacity, max splats, camera pose
- report coverage, overdraw, frame time
- export preview PNG

Client use:

- point-cloud visualization
- 3D scan preview
- neural-rendering concept demo
- sparse scene inspection

Reusable core:

```text
renderSplats(splats, camera, options) -> imageData + metrics
```

### 6. Cloth Constraint Sandbox

Current teaching demo: mass-spring cloth over a circle.

Production version:

- reusable position-based dynamics loop
- configurable pinned points, obstacles, gravity, timestep
- stretch and collision metrics
- deterministic reset and export final particle state

Client use:

- garment preview
- soft-object interaction prototype
- visual physics explainer

Reusable core:

```text
stepCloth(state, constraints, obstacles, options) -> state + metrics
```

### 7. Particle Fluid Sandbox

Current teaching demo: pressure and viscosity particles.

Production version:

- deterministic particle fixtures
- spatial hash neighbor lookup
- pressure, viscosity, boundary, and emitter modules
- report density error, neighbor count, frame time

Client use:

- liquid/sand/smoke intuition demo
- interactive material parameter tuning
- simulation performance tradeoff presentation

Reusable core:

```text
stepParticles(state, domain, options) -> state + metrics
```

### 8. Camera Projection And Calibration Lab

Current teaching demo: cube in two cameras.

Production version:

- load 3D landmarks and two camera poses
- project points into both views
- show reprojection error against observed 2D points
- adjust focal length, pose, baseline
- export calibrated camera parameters

Client use:

- AR alignment
- multi-camera capture
- robotics/inspection camera setup
- explaining why calibration matters

Reusable core:

```text
projectPoints(points3d, camera) -> points2d
reprojectionError(observed, predicted) -> metrics
```

### 9. Texture/Material Optimization

Current teaching demo: fit an 8x8 texture grid.

Production version:

- load target swatch or material image
- optimize texture grid with smoothness control
- compare pixel loss versus regularity
- export texture PNG and parameter grid

Client use:

- material matching
- defect camouflage
- asset texture fitting
- visual inspection parameter tuning

Reusable core:

```text
optimizeTexture(target, texture, options) -> { texture, lossHistory, metrics }
```

### 10. Motion Retargeting And Constraint Check

Current teaching demo: pose blend and scaled skeleton.

Production version:

- load source skeleton and target skeleton fixtures
- retarget joint angles with bone-length preservation
- add foot/contact constraints
- show foot sliding and pose error
- export retargeted motion frames

Client use:

- avatar animation transfer
- character control demo
- motion QA and artifact detection

Reusable core:

```text
retargetMotion(sourceFrames, sourceRig, targetRig, options) -> frames + metrics
```

## Author Code Policy

Original paper code can be valuable, but it should not be copied blindly.

For each paper family:

1. Find official project page or GitHub repository.
2. Record license, commit hash, install requirements, and model/data size.
3. Classify:
   - `link-only`: useful reference but not vendored
   - `wrapped`: can be called from a script without copying code
   - `adapted`: small licensed excerpt or reimplementation with attribution
   - `not-usable`: unclear license, broken install, missing data, or too heavy
4. Keep our demo runnable without requiring author code.

## Client Demo Packaging

Each production demo should support three modes:

- `explain`: default browser demo with text and controls
- `scenario`: client-shaped workflow with fixtures and before/after output
- `developer`: module API, input/output schema, tests, and integration notes

The page should say clearly:

```text
This demo is reusable for: scan cleanup, asset preview, calibration, etc.
What you would replace for a real client: input fixture, renderer, objective,
constraints, or performance target.
```

## First Implementation Milestone

Upgrade three demos first because they are broadly reusable and easy to explain
to clients:

1. Mesh cleanup for scanned/generated assets
2. Camera projection and calibration for AR/capture/inspection
3. Differentiable image fitting for inverse rendering and parameter estimation

Those three cover geometry, capture, and optimization. Once they are solid, use
the same module/spec/test pattern for the remaining seven.

