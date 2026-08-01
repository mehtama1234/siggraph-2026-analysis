import { makeCircleSamples } from "./core.js";

const TARGETS = [
  { x: -0.05, y: 0.04, radius: 0.34, intensity: 0.92, blur: 0.05 },
  { x: -0.38, y: -0.18, radius: 0.24, intensity: 0.72, blur: 0.045 },
  { x: 0.28, y: 0.22, radius: 0.42, intensity: 0.86, blur: 0.06 }
];

export function fittingFixture(preset = 0) {
  const target = TARGETS[Math.max(0, Math.min(TARGETS.length - 1, preset))];
  const initial = { x: 0.35, y: -0.24, radius: 0.18, intensity: 0.45, blur: target.blur };
  return { target, initial, samples: makeCircleSamples(target, 29) };
}
