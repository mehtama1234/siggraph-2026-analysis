import assert from "node:assert/strict";
import { fitParameters, imageLoss } from "../src/core.js";
import { fittingFixture } from "../src/fixtures.js";

const fixture = fittingFixture();
const before = imageLoss(fixture.samples, fixture.initial);
const result = fitParameters(fixture.samples, fixture.initial, { iterations: 140, step: 0.16 });

assert(result.metrics.finalLoss < before * 0.25, "fitting should substantially reduce image loss");
assert(Math.abs(result.params.x - fixture.target.x) < 0.18, "x should move toward target");
assert(Math.abs(result.params.y - fixture.target.y) < 0.18, "y should move toward target");

console.log("differentiable-rendering core tests passed");

