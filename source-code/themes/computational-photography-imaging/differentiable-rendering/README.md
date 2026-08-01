# Differentiable Rendering

Theme: Computational Photography & Imaging

This demo shows a render-and-correct loop. A guessed shape is rendered, compared
with a target image, and nudged by finite differences so the pixel error falls.
The image itself becomes the measurement used to update hidden parameters.

Run it from:

```text
../../../../index.html
```

Source:

```text
../../../../shared/siggraph-code-lab.js
```

