import assert from "node:assert/strict";
import { generateNoisyLoop, smoothMesh } from "../src/core.js";

const mesh = generateNoisyLoop(36, 1, 0.2);
const before = smoothMesh(mesh.vertices, mesh.edges, { iterations: 0 }).metrics;
const after = smoothMesh(mesh.vertices, mesh.edges, { iterations: 12, amount: 0.4, preserveArea: 0.6 }).metrics;

assert(after.roughness < before.roughness, "smoothing should reduce roughness");
assert(after.areaRatio > 0.65, "area preservation should avoid severe shrinkage");
assert(after.maxMovement > 0, "vertices should move");

console.log("laplacian-smoothing core tests passed");

