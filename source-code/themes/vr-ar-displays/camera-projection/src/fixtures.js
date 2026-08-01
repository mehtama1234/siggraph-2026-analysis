import { projectPoints } from "./core.js";

export function cubeLandmarks() {
  return [
    { x: -1, y: -1, z: 3 }, { x: 1, y: -1, z: 3 }, { x: 1, y: 1, z: 3 }, { x: -1, y: 1, z: 3 },
    { x: -1, y: -1, z: 5 }, { x: 1, y: -1, z: 5 }, { x: 1, y: 1, z: 5 }, { x: -1, y: 1, z: 5 }
  ];
}

export function calibrationFixture() {
  const points3d = cubeLandmarks();
  const trueCamera = { x: 0.32, y: 0, z: 0, yaw: 0.18, focal: 1.35, cx: 0, cy: 0 };
  const observed2d = projectPoints(points3d, trueCamera).map((p, i) => ({
    x: p.x + (i % 2 ? 0.006 : -0.004),
    y: p.y + (i % 3 ? -0.003 : 0.005)
  }));
  const initialCamera = { x: 0, y: 0, z: 0, yaw: -0.08, focal: 1.0, cx: 0, cy: 0 };
  return { points3d, observed2d, trueCamera, initialCamera };
}

