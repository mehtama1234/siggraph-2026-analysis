# SIGGRAPH Code Companion

This folder adds runnable examples for the SIGGRAPH first-principles writeups.
The goal is not to reproduce full papers. Each demo is a small, readable proof
of the mathematical idea behind a theme or subtheme.

Open the lab:

```text
source-code/index.html
```

Live site path after GitHub Pages updates:

```text
https://mehtama1234.github.io/siggraph-2026-analysis/source-code/
```

## Demo Standard

Each demo should show one visible story:

```text
before -> mechanism -> after
```

Every example should be:

- end-user friendly: sliders, buttons, and visible output
- first-principles: explain the object, the rule, and the tradeoff
- compact: small enough to read in one sitting
- honest: toy code, not claimed as a paper reproduction
- mapped: connected to a SIGGRAPH theme, subtheme, and nearby paper family

## Current Demos

- Rendering and Light Transport / ray marching
- Geometry Processing and Meshes / Laplacian smoothing
- Neural Fields and Representations / signed distance fields
- Computational Photography and Imaging / differentiable rendering
- Neural Rendering and Radiance Fields / Gaussian splatting
- Cloth, Hair and Fibers / mass-spring cloth
- Fluids, Smoke and Granular / particle fluids
- VR/AR and Displays / camera projection
- Appearance, Materials and BRDF / texture optimization
- Character Animation and Motion / motion interpolation and retargeting

## Source Layout

```text
source-code/
  index.html
  theme-index.json
  shared/
    siggraph-code-lab.js
  themes/
    rendering-light-transport/ray-marching/
    geometry-processing-meshes/laplacian-smoothing/
    neural-fields-representations/signed-distance-fields/
    computational-photography-imaging/differentiable-rendering/
    neural-rendering-radiance-fields/gaussian-splatting/
    cloth-hair-fibers/mass-spring-cloth/
    fluids-smoke-granular/particle-fluids/
    vr-ar-displays/camera-projection/
    appearance-materials-brdf/texture-optimization/
    character-animation-motion/motion-interpolation-retargeting/
```

