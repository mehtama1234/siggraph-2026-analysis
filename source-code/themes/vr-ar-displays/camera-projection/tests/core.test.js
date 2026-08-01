import assert from "node:assert/strict";
import { calibrateCamera, projectPoints, reprojectionError } from "../src/core.js";
import { calibrationFixture } from "../src/fixtures.js";

const fixture = calibrationFixture();
const before = reprojectionError(fixture.observed2d, projectPoints(fixture.points3d, fixture.initialCamera));
const result = calibrateCamera(fixture.points3d, fixture.observed2d, fixture.initialCamera, { iterations: 100, step: 0.06 });

assert(result.metrics.rmse < before.rmse, "calibration should reduce reprojection RMSE");
assert(result.metrics.rmse < 0.05, "calibrated reprojection error should be small for fixture");
assert(result.camera.focal > 0, "focal length must remain positive");

console.log("camera-projection core tests passed");

