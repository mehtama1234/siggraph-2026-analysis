# Texture Optimization

Theme: Appearance, Materials & BRDF

This demo treats a texture as a grid of adjustable values. The optimizer compares
the current rendered pattern with a target pattern, then changes each cell toward
the color that lowers the residual while optional smoothing keeps neighboring
cells coherent.

Run it from:

```text
../../../../index.html
```

Source:

```text
../../../../shared/siggraph-code-lab.js
```

