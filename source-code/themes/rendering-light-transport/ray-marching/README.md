# Ray Marching

Theme: Rendering & Light Transport

This demo shows how a renderer can find a surface without a triangle mesh. A ray
asks a signed distance field how far it can safely move. Large empty regions are
crossed quickly; near a surface, the steps become small. Once the ray hits, the
surface normal and light direction determine the shade.

Run it from:

```text
../../../../index.html
```

Source:

```text
../../../../shared/siggraph-code-lab.js
```

