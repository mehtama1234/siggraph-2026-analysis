export function projectPoint(point, camera) {
  const yaw = camera.yaw ?? 0;
  const focal = camera.focal ?? 1;
  const cx = camera.cx ?? 0;
  const cy = camera.cy ?? 0;
  const camX = camera.x ?? 0;
  const camY = camera.y ?? 0;
  const camZ = camera.z ?? 0;
  const x0 = point.x - camX;
  const y0 = point.y - camY;
  const z0 = point.z - camZ;
  const x = x0 * Math.cos(yaw) - z0 * Math.sin(yaw);
  const z = x0 * Math.sin(yaw) + z0 * Math.cos(yaw);
  return {
    x: cx + focal * x / z,
    y: cy + focal * y0 / z,
    depth: z
  };
}

export function projectPoints(points, camera) {
  return points.map((p) => projectPoint(p, camera));
}

export function reprojectionError(observed, predicted) {
  let sum = 0;
  let max = 0;
  for (let i = 0; i < observed.length; i++) {
    const e = Math.hypot(observed[i].x - predicted[i].x, observed[i].y - predicted[i].y);
    sum += e * e;
    max = Math.max(max, e);
  }
  return {
    rmse: Math.sqrt(sum / observed.length),
    max
  };
}

export function calibrateCamera(points3d, observed2d, initial, options = {}) {
  const iterations = options.iterations ?? 80;
  const step = options.step ?? 0.08;
  const eps = options.eps ?? 0.001;
  const params = { ...initial };
  const keys = options.keys ?? ["yaw", "focal", "x"];
  const history = [];

  const loss = (p) => {
    const predicted = projectPoints(points3d, p);
    const err = reprojectionError(observed2d, predicted);
    return err.rmse;
  };

  for (let it = 0; it < iterations; it++) {
    const base = loss(params);
    history.push(base);
    const grads = {};
    for (const key of keys) {
      const probe = { ...params, [key]: params[key] + eps };
      grads[key] = (loss(probe) - base) / eps;
    }
    let accepted = false;
    for (let scale = step; scale > 1e-5; scale *= 0.5) {
      const trial = { ...params };
      for (const key of keys) trial[key] -= scale * grads[key];
      trial.focal = Math.max(0.2, Math.min(4, trial.focal));
      trial.yaw = Math.max(-1.2, Math.min(1.2, trial.yaw));
      trial.x = Math.max(-2, Math.min(2, trial.x));
      if (loss(trial) <= base) {
        Object.assign(params, trial);
        accepted = true;
        break;
      }
    }
    if (!accepted) break;
  }

  const predicted = projectPoints(points3d, params);
  return {
    camera: params,
    predicted,
    metrics: {
      ...reprojectionError(observed2d, predicted),
      iterations,
      initialRmse: history[0],
      finalRmse: history[history.length - 1]
    },
    history
  };
}
