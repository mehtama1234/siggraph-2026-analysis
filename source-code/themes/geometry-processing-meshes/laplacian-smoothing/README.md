# Laplacian Smoothing

Theme: Geometry Processing & Meshes

This demo shows the neighbor-average idea behind many mesh cleanup methods. It
is now backed by a reusable starter module for client-style scan or generated
asset cleanup.

Run it from:

```text
../../../../index.html
```

Reusable API:

```text
src/core.js
smoothMesh(vertices, edges, options) -> { vertices, metrics }
```

Test:

```text
node tests/core.test.js
```
