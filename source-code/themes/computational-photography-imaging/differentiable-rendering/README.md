# Differentiable Rendering

Theme: Computational Photography & Imaging

This demo shows a render-and-correct loop. A guessed shape is rendered, compared
with a target image, and nudged by finite differences so the pixel error falls.
It is now backed by a reusable starter module for client-style inverse rendering
or visual parameter fitting.

Run it from:

```text
../../../../index.html
```

Reusable API:

```text
src/core.js
fitParameters(targetSamples, initialParams, options) -> { params, lossHistory, metrics }
```

Test:

```text
node tests/core.test.js
```
