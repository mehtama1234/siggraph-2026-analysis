# Camera Projection

Theme: VR/AR & Displays

This demo shows how 3D points become 2D screen points and how camera parameters
can be adjusted to reduce reprojection error. It is now backed by a reusable
starter module for AR, capture, or inspection alignment.

Run it from:

```text
../../../../index.html
```

Reusable API:

```text
src/core.js
projectPoints(points3d, camera) -> points2d
calibrateCamera(points3d, observed2d, initial, options) -> result
```

Test:

```text
node tests/core.test.js
```
