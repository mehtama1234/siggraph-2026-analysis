import { generateNoisyLoop } from "./core.js";

export function defaultMeshFixture() {
  return generateNoisyLoop(36, 1, 0.2);
}

export function productOutlineFixture() {
  const vertices = [
    { x: -0.95, y: -0.45 }, { x: -0.65, y: -0.55 }, { x: -0.34, y: -0.50 },
    { x: -0.12, y: -0.68 }, { x: 0.12, y: -0.52 }, { x: 0.48, y: -0.56 },
    { x: 0.82, y: -0.38 }, { x: 0.92, y: -0.08 }, { x: 0.76, y: 0.18 },
    { x: 0.88, y: 0.48 }, { x: 0.48, y: 0.58 }, { x: 0.15, y: 0.47 },
    { x: -0.12, y: 0.66 }, { x: -0.42, y: 0.50 }, { x: -0.72, y: 0.54 },
    { x: -0.96, y: 0.28 }, { x: -0.84, y: 0.02 }
  ];
  const edges = vertices.map((_, i) => [i, (i + 1) % vertices.length]);
  return { vertices, edges };
}
