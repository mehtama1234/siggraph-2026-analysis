export function clamp01(v) {
  return Math.max(0, Math.min(1, v));
}

export function softCircle(x, y, params) {
  const blur = params.blur ?? 0.04;
  const d = Math.hypot(x - params.x, y - params.y);
  return clamp01((params.radius - d) / blur + 0.5) * params.intensity;
}

export function imageLoss(samples, params) {
  let loss = 0;
  for (const s of samples) {
    const predicted = softCircle(s.x, s.y, params);
    const e = predicted - s.value;
    loss += e * e;
  }
  return loss / samples.length;
}

export function fitParameters(samples, initial, options = {}) {
  const params = { ...initial };
  const keys = options.keys ?? ["x", "y", "radius", "intensity"];
  const iterations = options.iterations ?? 100;
  const step = options.step ?? 0.18;
  const eps = options.eps ?? 0.001;
  const history = [];

  for (let it = 0; it < iterations; it++) {
    const base = imageLoss(samples, params);
    history.push(base);
    const grads = {};
    for (const key of keys) {
      const hi = { ...params, [key]: params[key] + eps };
      const lo = { ...params, [key]: params[key] - eps };
      grads[key] = (imageLoss(samples, hi) - imageLoss(samples, lo)) / (2 * eps);
    }
    let accepted = false;
    for (let scale = step; scale > 1e-5; scale *= 0.5) {
      const trial = { ...params };
      for (const key of keys) trial[key] -= scale * grads[key];
      trial.x = Math.max(-1, Math.min(1, trial.x));
      trial.y = Math.max(-1, Math.min(1, trial.y));
      trial.radius = Math.max(0.05, Math.min(0.75, trial.radius));
      trial.intensity = clamp01(trial.intensity);
      if (imageLoss(samples, trial) <= base) {
        Object.assign(params, trial);
        accepted = true;
        break;
      }
    }
    if (!accepted) break;
  }

  return {
    params,
    lossHistory: history,
    metrics: {
      initialLoss: history[0],
      finalLoss: history[history.length - 1],
      iterations
    }
  };
}

export function makeCircleSamples(target, grid = 25) {
  const samples = [];
  for (let y = 0; y < grid; y++) {
    for (let x = 0; x < grid; x++) {
      const px = (x / (grid - 1)) * 2 - 1;
      const py = (y / (grid - 1)) * 2 - 1;
      samples.push({ x: px, y: py, value: softCircle(px, py, target) });
    }
  }
  return samples;
}
