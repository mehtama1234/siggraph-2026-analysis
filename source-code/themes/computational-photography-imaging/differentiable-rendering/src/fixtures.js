import { makeCircleSamples } from "./core.js";

export function fittingFixture() {
  const target = { x: -0.05, y: 0.04, radius: 0.34, intensity: 0.92, blur: 0.05 };
  const initial = { x: 0.35, y: -0.24, radius: 0.18, intensity: 0.45, blur: 0.05 };
  return { target, initial, samples: makeCircleSamples(target, 29) };
}

