const canvas = document.getElementById("labCanvas");
const ctx = canvas.getContext("2d");
const tabs = document.getElementById("demoTabs");
const titleEl = document.getElementById("demoTitle");
const themeEl = document.getElementById("demoTheme");
const explainEl = document.getElementById("demoExplain");
const metricsEl = document.getElementById("metrics");
const controlsEl = document.getElementById("controls");
const buttonsEl = document.getElementById("buttons");
const folderLink = document.getElementById("folderLink");

const TAU = Math.PI * 2;
let active = 0;
let frame = 0;
let running = true;

function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
function lerp(a, b, t) { return a + (b - a) * t; }
function hypot(x, y) { return Math.sqrt(x * x + y * y); }

const demos = [
  {
    id: "ray-marching",
    title: "Ray Marching",
    theme: "Rendering & Light Transport",
    folder: "themes/rendering-light-transport/ray-marching/",
    explain: "A ray moves through space by asking a distance field how far it can safely step. Small steps near the surface reveal the hit point, then a light direction turns the surface normal into shading.",
    controls: { radius: [0.18, 0.38, 0.26, 0.01], light: [-1, 1, 0.35, 0.01], softness: [0, 1, 0.35, 0.01] },
    metrics: () => ({ "hit pixels": state.rayHits || 0, "avg steps": (state.raySteps || 0).toFixed(1) }),
    draw: drawRayMarch
  },
  {
    id: "laplacian-smoothing",
    title: "Laplacian Mesh Smoothing",
    theme: "Geometry Processing & Meshes",
    folder: "themes/geometry-processing-meshes/laplacian-smoothing/",
    explain: "Each vertex asks its neighbors where the local average is, then moves partway toward it. Noise disappears because local spikes disagree with their neighbors, but the whole shape shrinks unless boundary or volume constraints push back.",
    controls: { amount: [0, 1, 0.45, 0.01], iterations: [0, 40, 14, 1], preserve: [0, 1, 0.45, 0.01] },
    metrics: () => ({ roughness: state.meshRough.toFixed(2), shrink: state.meshShrink.toFixed(2) }),
    init: initMesh,
    draw: drawMesh
  },
  {
    id: "signed-distance-fields",
    title: "Signed Distance Fields",
    theme: "Neural Fields & Representations",
    folder: "themes/neural-fields-representations/signed-distance-fields/",
    explain: "A shape can be stored as a question: how far am I from the surface, and am I inside or outside? Union, intersection, and subtraction are simple min/max rules over those distances.",
    controls: { blend: [0, 1, 0.2, 0.01], box: [0.12, 0.38, 0.24, 0.01], operation: [0, 2, 0, 1] },
    metrics: () => ({ inside: state.sdfInside || 0, edge: state.sdfEdge || 0 }),
    draw: drawSdf
  },
  {
    id: "differentiable-rendering",
    title: "Differentiable Rendering",
    theme: "Computational Photography & Imaging",
    folder: "themes/computational-photography-imaging/differentiable-rendering/",
    explain: "Render a guess, compare it with a target image, then nudge the hidden parameters in the direction that makes the image error smaller. The picture becomes the measuring instrument.",
    controls: { speed: [0.1, 2.5, 0.9, 0.1], blur: [0.01, 0.08, 0.035, 0.005] },
    metrics: () => ({ loss: state.diffLoss.toFixed(3), steps: state.diffSteps }),
    init: initDiff,
    draw: drawDiff,
    buttons: [{ label: "Optimize", primary: true, action: () => state.diffRun = !state.diffRun }, { label: "Reset", action: initDiff }]
  },
  {
    id: "gaussian-splatting",
    title: "Gaussian Splatting",
    theme: "Neural Rendering & Radiance Fields",
    folder: "themes/neural-rendering-radiance-fields/gaussian-splatting/",
    explain: "A scene is painted by many soft colored blobs. Each blob contributes most near its center and fades with distance; depth order decides which translucent color has more say.",
    controls: { splats: [8, 80, 38, 1], size: [8, 52, 26, 1], depth: [0, 1, 0.55, 0.01] },
    metrics: () => ({ splats: controls.splats, coverage: `${state.splatCoverage || 0}%` }),
    init: initSplats,
    draw: drawSplats,
    buttons: [{ label: "New blobs", action: initSplats }]
  },
  {
    id: "mass-spring-cloth",
    title: "Mass-Spring Cloth",
    theme: "Cloth, Hair & Fibers",
    folder: "themes/cloth-hair-fibers/mass-spring-cloth/",
    explain: "Cloth is a grid of points connected by springs. Gravity pulls down, springs resist stretching, damping removes jitter, and collision stops the sheet from passing through an obstacle.",
    controls: { stiffness: [0.05, 0.35, 0.18, 0.01], damping: [0.94, 0.995, 0.975, 0.001], gravity: [0, 1.2, 0.55, 0.01] },
    metrics: () => ({ stretch: state.clothStretch.toFixed(2), collisions: state.clothCollisions }),
    init: initCloth,
    draw: drawCloth,
    buttons: [{ label: "Reset cloth", action: initCloth }]
  },
  {
    id: "particle-fluids",
    title: "Particle Fluids",
    theme: "Fluids, Smoke & Granular",
    folder: "themes/fluids-smoke-granular/particle-fluids/",
    explain: "Each particle pushes neighbors away when crowded and borrows velocity from neighbors when viscous. The visible behavior comes from many local corrections, not from one global water rule.",
    controls: { pressure: [0.1, 1.8, 0.85, 0.01], viscosity: [0, 0.16, 0.045, 0.005], flow: [0, 1, 0.5, 0.01] },
    metrics: () => ({ particles: state.fluid.length, crowding: state.fluidCrowd.toFixed(2) }),
    init: initFluid,
    draw: drawFluid,
    buttons: [{ label: "Pour again", action: initFluid }]
  },
  {
    id: "camera-projection",
    title: "Camera Projection",
    theme: "VR/AR & Displays",
    folder: "themes/vr-ar-displays/camera-projection/",
    explain: "A camera turns a 3D point into a 2D screen point by dividing by depth. Move the camera and nearby points slide more than far points; that parallax is the clue used to recover depth.",
    controls: { yaw: [-0.8, 0.8, 0.25, 0.01], baseline: [0, 1.2, 0.55, 0.01], focal: [0.8, 2.0, 1.25, 0.01] },
    metrics: () => ({ parallax: state.parallax.toFixed(2), points: 8 }),
    draw: drawCamera
  },
  {
    id: "texture-optimization",
    title: "Texture Optimization",
    theme: "Appearance, Materials & BRDF",
    folder: "themes/appearance-materials-brdf/texture-optimization/",
    explain: "A texture is a grid of parameters. The optimizer compares the rendered pattern with a target and updates each cell toward the color that would reduce the image residual.",
    controls: { rate: [0.02, 0.35, 0.12, 0.01], smooth: [0, 0.35, 0.08, 0.01], target: [0, 2, 0, 1] },
    metrics: () => ({ loss: state.texLoss.toFixed(3), cells: 64 }),
    init: initTexture,
    draw: drawTexture,
    buttons: [{ label: "Optimize", primary: true, action: () => state.texRun = !state.texRun }, { label: "Reset", action: initTexture }]
  },
  {
    id: "motion-retargeting",
    title: "Motion Retargeting",
    theme: "Character Animation & Motion",
    folder: "themes/character-animation-motion/motion-interpolation-retargeting/",
    explain: "A pose is a chain of joint angles and bone lengths. Interpolation blends angles over time; retargeting keeps the angles but changes the bone lengths so the motion fits another body.",
    controls: { blend: [0, 1, 0.5, 0.01], scale: [0.65, 1.45, 1.1, 0.01], constraint: [0, 1, 0.7, 0.01] },
    metrics: () => ({ footSlide: state.footSlide.toFixed(2), bones: 5 }),
    draw: drawMotion
  }
];

let controls = {};
let state = {};

function setup() {
  tabs.innerHTML = "";
  demos.forEach((demo, i) => {
    const b = document.createElement("button");
    b.className = "demo-tab";
    b.type = "button";
    b.setAttribute("aria-selected", i === active ? "true" : "false");
    b.innerHTML = `${demo.title}<span>${demo.theme}</span>`;
    b.addEventListener("click", () => selectDemo(i));
    tabs.appendChild(b);
  });
  selectDemo(0);
  requestAnimationFrame(tick);
}

function selectDemo(i) {
  active = i;
  const demo = demos[active];
  controls = {};
  for (const [name, cfg] of Object.entries(demo.controls || {})) controls[name] = cfg[2];
  state = {};
  titleEl.textContent = demo.title;
  themeEl.textContent = `${demo.theme} / ${demo.id}`;
  explainEl.textContent = demo.explain;
  folderLink.href = demo.folder;
  renderControls(demo);
  if (demo.init) demo.init();
  [...tabs.children].forEach((b, idx) => b.setAttribute("aria-selected", idx === active ? "true" : "false"));
  draw();
}

function renderControls(demo) {
  controlsEl.innerHTML = "";
  for (const [name, cfg] of Object.entries(demo.controls || {})) {
    const [min, max, value, step] = cfg;
    const wrap = document.createElement("div");
    wrap.className = "control";
    const label = document.createElement("label");
    const val = document.createElement("span");
    val.textContent = value;
    label.innerHTML = `<span>${name}</span>`;
    label.appendChild(val);
    const input = document.createElement("input");
    input.type = "range";
    input.min = min;
    input.max = max;
    input.step = step;
    input.value = value;
    input.addEventListener("input", () => {
      controls[name] = Number(input.value);
      val.textContent = input.value;
      draw();
    });
    wrap.appendChild(label);
    wrap.appendChild(input);
    controlsEl.appendChild(wrap);
  }
  buttonsEl.innerHTML = "";
  for (const spec of demo.buttons || []) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = `action${spec.primary ? " primary" : ""}`;
    btn.textContent = spec.label;
    btn.addEventListener("click", () => { spec.action(); draw(); });
    buttonsEl.appendChild(btn);
  }
}

function updateMetrics() {
  const m = demos[active].metrics ? demos[active].metrics() : {};
  metricsEl.innerHTML = "";
  for (const [k, v] of Object.entries(m)) {
    const d = document.createElement("div");
    d.className = "metric";
    d.innerHTML = `<b>${k}</b><span>${v}</span>`;
    metricsEl.appendChild(d);
  }
}

function clear() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "#f3f6f8";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function draw() {
  clear();
  demos[active].draw();
  updateMetrics();
}

function tick() {
  frame++;
  const id = demos[active].id;
  if (running && ["mass-spring-cloth", "particle-fluids", "differentiable-rendering", "texture-optimization"].includes(id)) draw();
  requestAnimationFrame(tick);
}

function drawRayMarch() {
  const w = canvas.width, h = canvas.height;
  const img = ctx.createImageData(w, h);
  let hits = 0, stepsTotal = 0;
  const radius = controls.radius;
  const lx = controls.light, ly = -0.85;
  for (let y = 0; y < h; y += 2) {
    for (let x = 0; x < w; x += 2) {
      const px = (x / w) * 2 - 1;
      const py = (y / h) * 1.5 - 0.75;
      let t = 0, hit = false, steps = 0;
      for (; steps < 44; steps++) {
        const rx = px * (1 + t * 0.15);
        const ry = py;
        const d = hypot(rx, ry) - radius;
        if (d < 0.002) { hit = true; break; }
        t += d * (0.55 + controls.softness * 0.35);
        if (t > 2.8) break;
      }
      let r = 218, g = 228, b = 236;
      if (hit) {
        hits++;
        stepsTotal += steps;
        const nx = px / Math.max(radius, 0.01), ny = py / Math.max(radius, 0.01);
        const nl = clamp((nx * lx + ny * ly) / hypot(lx, ly), -1, 1);
        const shade = clamp(0.32 + 0.68 * nl, 0.12, 1);
        r = 48 * shade; g = 128 * shade; b = 118 * shade;
      }
      for (let yy = 0; yy < 2; yy++) for (let xx = 0; xx < 2; xx++) {
        const i = ((y + yy) * w + x + xx) * 4;
        img.data[i] = r; img.data[i + 1] = g; img.data[i + 2] = b; img.data[i + 3] = 255;
      }
    }
  }
  ctx.putImageData(img, 0, 0);
  drawLabel("ray steps stop when distance is almost zero", 26, 34);
  state.rayHits = hits * 4;
  state.raySteps = hits ? stepsTotal / hits : 0;
}

function initMesh() {
  state.mesh = [];
  for (let i = 0; i < 34; i++) {
    const a = i / 34 * TAU;
    const r = 205 + Math.sin(i * 2.1) * 40 + Math.cos(i * 4.7) * 18;
    state.mesh.push({ x: 480 + Math.cos(a) * r, y: 360 + Math.sin(a) * r, bx: 480 + Math.cos(a) * r, by: 360 + Math.sin(a) * r });
  }
}

function drawMesh() {
  if (!state.mesh) initMesh();
  let pts = state.mesh.map(p => ({ x: p.bx, y: p.by }));
  const originalArea = polyArea(pts);
  for (let it = 0; it < controls.iterations; it++) {
    const next = pts.map((p, i) => {
      const a = pts[(i + pts.length - 1) % pts.length], b = pts[(i + 1) % pts.length];
      const ax = (a.x + b.x) / 2, ay = (a.y + b.y) / 2;
      const cx = 480 + (p.x - 480) * (1 + controls.preserve * 0.018);
      const cy = 360 + (p.y - 360) * (1 + controls.preserve * 0.018);
      return { x: lerp(cx, ax, controls.amount), y: lerp(cy, ay, controls.amount) };
    });
    pts = next;
  }
  polygon(state.mesh.map(p => ({ x: p.bx, y: p.by })), "#9a3412", 2, "rgba(154,52,18,0.08)");
  polygon(pts, "#0f766e", 4, "rgba(15,118,110,0.15)");
  state.meshRough = roughness(pts);
  state.meshShrink = polyArea(pts) / originalArea;
  drawLabel("orange: original noisy mesh   green: neighbor-averaged mesh", 26, 34);
}

function drawSdf() {
  const w = canvas.width, h = canvas.height;
  const cell = 8;
  let inside = 0, edge = 0;
  for (let y = 0; y < h; y += cell) {
    for (let x = 0; x < w; x += cell) {
      const px = (x / w) * 2 - 1, py = (y / h) * 1.5 - 0.75;
      const circle = hypot(px + 0.18, py) - 0.36;
      const bx = Math.abs(px - 0.22) - controls.box;
      const by = Math.abs(py + 0.02) - controls.box * 0.75;
      const box = Math.max(bx, by);
      let d = Math.min(circle, box);
      if (controls.operation === 1) d = Math.max(circle, box);
      if (controls.operation === 2) d = Math.max(circle, -box);
      d -= controls.blend * 0.03;
      if (d < 0) inside++;
      if (Math.abs(d) < 0.018) edge++;
      const shade = clamp(220 - d * 320, 35, 245);
      ctx.fillStyle = d < 0 ? `rgb(${40 + shade * 0.25},${110 + shade * 0.25},${105 + shade * 0.2})` : `rgb(${shade},${shade + 4},${shade + 8})`;
      ctx.fillRect(x, y, cell + 1, cell + 1);
    }
  }
  state.sdfInside = inside;
  state.sdfEdge = edge;
  drawLabel(["union: nearest surface wins", "intersection: must be inside both", "subtraction: inside circle but outside box"][controls.operation], 26, 34);
}

function initDiff() {
  state.diff = { x: 0.28, y: -0.16, r: 0.20, c: 0.25 };
  state.diffRun = false;
  state.diffSteps = 0;
  state.diffLoss = 1;
}

function targetCircle(x, y) {
  return smoothCircle(x + 0.04, y - 0.02, 0.27, 0.035);
}

function guessCircle(x, y, p) {
  return p.c * smoothCircle(x - p.x, y - p.y, p.r, controls.blur);
}

function lossDiff(p) {
  let loss = 0, n = 0;
  for (let yy = -0.65; yy <= 0.65; yy += 0.08) for (let xx = -0.9; xx <= 0.9; xx += 0.08) {
    const e = guessCircle(xx, yy, p) - targetCircle(xx, yy);
    loss += e * e; n++;
  }
  return loss / n;
}

function drawDiff() {
  if (!state.diff) initDiff();
  if (state.diffRun) {
    const p = state.diff, base = lossDiff(p), eps = 0.01;
    for (const k of ["x", "y", "r", "c"]) {
      const q = { ...p }; q[k] += eps;
      const g = (lossDiff(q) - base) / eps;
      p[k] -= controls.speed * 0.12 * g;
    }
    p.r = clamp(p.r, 0.08, 0.42); p.c = clamp(p.c, 0.05, 1.2);
    state.diffSteps++;
  }
  const w = canvas.width, h = canvas.height, img = ctx.createImageData(w, h);
  for (let y = 0; y < h; y += 2) for (let x = 0; x < w; x += 2) {
    const px = (x / w) * 2 - 1, py = (y / h) * 1.5 - 0.75;
    const t = targetCircle(px, py), g = guessCircle(px, py, state.diff);
    const r = 245 - t * 120 + g * 40, gr = 245 - g * 120, b = 245 - t * 120;
    fillBlock(img, w, x, y, 2, r, gr, b);
  }
  ctx.putImageData(img, 0, 0);
  state.diffLoss = lossDiff(state.diff);
  drawLabel("red target + green guess; optimize lowers pixel error", 26, 34);
}

function initSplats() {
  state.splats = Array.from({ length: 90 }, (_, i) => ({
    x: 160 + Math.random() * 640,
    y: 130 + Math.random() * 460,
    z: Math.random(),
    c: [`hsl(${175 + i * 9 % 160},70%,48%)`, `hsl(${20 + i * 7 % 80},75%,55%)`][i % 2]
  }));
}

function drawSplats() {
  if (!state.splats) initSplats();
  ctx.fillStyle = "#eef3f7"; ctx.fillRect(0, 0, canvas.width, canvas.height);
  const count = controls.splats;
  const arr = state.splats.slice(0, count).sort((a, b) => controls.depth ? a.z - b.z : b.z - a.z);
  for (const s of arr) {
    const rad = controls.size * (0.75 + s.z * 0.7);
    const grad = ctx.createRadialGradient(s.x, s.y, 0, s.x, s.y, rad);
    grad.addColorStop(0, s.c.replace(")", ",0.50)").replace("hsl", "hsla"));
    grad.addColorStop(1, s.c.replace(")", ",0)").replace("hsl", "hsla"));
    ctx.fillStyle = grad;
    ctx.beginPath(); ctx.arc(s.x, s.y, rad, 0, TAU); ctx.fill();
  }
  state.splatCoverage = Math.round(clamp(count * controls.size / 20, 0, 100));
  drawLabel("soft kernels add up into an image; order changes visibility", 26, 34);
}

function initCloth() {
  const cols = 16, rows = 11, gap = 32;
  state.cloth = [];
  for (let y = 0; y < rows; y++) for (let x = 0; x < cols; x++) {
    state.cloth.push({ x: 230 + x * gap, y: 80 + y * gap, px: 230 + x * gap, py: 80 + y * gap, pin: y === 0 && (x === 0 || x === cols - 1) });
  }
  state.clothCols = cols; state.clothRows = rows;
}

function drawCloth() {
  if (!state.cloth) initCloth();
  const pts = state.cloth, cols = state.clothCols, gap = 32;
  let collisions = 0, stretch = 0;
  for (const p of pts) {
    if (p.pin) continue;
    const vx = (p.x - p.px) * controls.damping, vy = (p.y - p.py) * controls.damping;
    p.px = p.x; p.py = p.y;
    p.x += vx; p.y += vy + controls.gravity;
  }
  for (let k = 0; k < 3; k++) {
    for (let i = 0; i < pts.length; i++) {
      if (i % cols !== cols - 1) solveSpring(pts[i], pts[i + 1], gap, controls.stiffness);
      if (i + cols < pts.length) solveSpring(pts[i], pts[i + cols], gap, controls.stiffness);
    }
  }
  for (const p of pts) {
    const dx = p.x - 480, dy = p.y - 430, d = hypot(dx, dy), r = 105;
    if (d < r) { const s = r / Math.max(d, 0.001); p.x = 480 + dx * s; p.y = 430 + dy * s; collisions++; }
  }
  ctx.strokeStyle = "#64748b"; ctx.lineWidth = 1.2;
  for (let i = 0; i < pts.length; i++) {
    if (i % cols !== cols - 1) line(pts[i], pts[i + 1]);
    if (i + cols < pts.length) line(pts[i], pts[i + cols]);
  }
  ctx.fillStyle = "rgba(154,52,18,0.18)"; ctx.beginPath(); ctx.arc(480, 430, 105, 0, TAU); ctx.fill();
  for (let i = 0; i < pts.length; i++) if (i % cols !== cols - 1) stretch += Math.abs(hypot(pts[i].x - pts[i + 1].x, pts[i].y - pts[i + 1].y) - gap);
  state.clothStretch = stretch / pts.length;
  state.clothCollisions = collisions;
  drawLabel("springs pull neighbors back to their rest distance", 26, 34);
}

function initFluid() {
  state.fluid = [];
  for (let i = 0; i < 80; i++) state.fluid.push({ x: 300 + Math.random() * 80, y: 120 + Math.random() * 60, vx: Math.random() * 2, vy: 0 });
}

function drawFluid() {
  if (!state.fluid) initFluid();
  const ps = state.fluid;
  let crowd = 0;
  for (const p of ps) { p.vy += 0.18; p.vx += controls.flow * 0.025; }
  for (let i = 0; i < ps.length; i++) for (let j = i + 1; j < ps.length; j++) {
    const a = ps[i], b = ps[j], dx = b.x - a.x, dy = b.y - a.y, d = hypot(dx, dy), r = 22;
    if (d < r && d > 0.01) {
      const push = (r - d) / r * controls.pressure;
      const nx = dx / d, ny = dy / d;
      a.vx -= nx * push; a.vy -= ny * push; b.vx += nx * push; b.vy += ny * push;
      const mix = controls.viscosity;
      const avx = (a.vx + b.vx) / 2, avy = (a.vy + b.vy) / 2;
      a.vx = lerp(a.vx, avx, mix); a.vy = lerp(a.vy, avy, mix); b.vx = lerp(b.vx, avx, mix); b.vy = lerp(b.vy, avy, mix);
      crowd += push;
    }
  }
  ctx.fillStyle = "#e7eef4"; ctx.fillRect(170, 95, 620, 510);
  ctx.strokeStyle = "#334155"; ctx.lineWidth = 3; ctx.strokeRect(170, 95, 620, 510);
  for (const p of ps) {
    p.x += p.vx; p.y += p.vy;
    if (p.x < 185 || p.x > 775) { p.vx *= -0.55; p.x = clamp(p.x, 185, 775); }
    if (p.y > 590) { p.vy *= -0.42; p.y = 590; p.vx *= 0.985; }
    ctx.fillStyle = "#0f766e"; ctx.beginPath(); ctx.arc(p.x, p.y, 6, 0, TAU); ctx.fill();
  }
  state.fluidCrowd = crowd / ps.length;
  drawLabel("pressure separates crowded particles; viscosity shares velocity", 26, 34);
}

function drawCamera() {
  const pts = [[-1,-1,2], [1,-1,2], [1,1,2], [-1,1,2], [-1,-1,4], [1,-1,4], [1,1,4], [-1,1,4]];
  const edges = [[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]];
  const yaw = controls.yaw, f = controls.focal, b = controls.baseline;
  const left = pts.map(p => project(p, -b / 2, yaw, f, 260, 360));
  const right = pts.map(p => project(p, b / 2, yaw, f, 700, 360));
  ctx.fillStyle = "#fff"; ctx.fillRect(75, 90, 360, 500); ctx.fillRect(525, 90, 360, 500);
  ctx.strokeStyle = "#cbd5e1"; ctx.strokeRect(75, 90, 360, 500); ctx.strokeRect(525, 90, 360, 500);
  drawEdges(left, edges, "#0f766e"); drawEdges(right, edges, "#9a3412");
  let par = 0; for (let i = 0; i < pts.length; i++) par += Math.abs(left[i].x - (right[i].x - 440));
  state.parallax = par / pts.length;
  drawLabel("left and right views disagree more when baseline grows", 26, 34);
}

function initTexture() {
  state.tex = Array.from({ length: 64 }, () => Math.random() * 0.25 + 0.35);
  state.texRun = false;
  state.texLoss = 1;
}

function texTarget(i) {
  const x = i % 8, y = Math.floor(i / 8);
  if (controls.target === 1) return ((x + y) % 2) ? 0.2 : 0.9;
  if (controls.target === 2) return hypot(x - 3.5, y - 3.5) < 2.5 ? 0.85 : 0.25;
  return x < 4 ? 0.25 + y * 0.06 : 0.85 - y * 0.04;
}

function drawTexture() {
  if (!state.tex) initTexture();
  if (state.texRun) {
    const next = state.tex.slice();
    for (let i = 0; i < 64; i++) {
      const x = i % 8, y = Math.floor(i / 8);
      let avg = state.tex[i], n = 1;
      for (const [dx, dy] of [[1,0],[-1,0],[0,1],[0,-1]]) {
        const xx = x + dx, yy = y + dy;
        if (xx >= 0 && xx < 8 && yy >= 0 && yy < 8) { avg += state.tex[yy * 8 + xx]; n++; }
      }
      const target = texTarget(i);
      next[i] += controls.rate * (target - state.tex[i]) + controls.smooth * (avg / n - state.tex[i]);
    }
    state.tex = next.map(v => clamp(v, 0, 1));
  }
  let loss = 0;
  drawGrid(110, 120, "target", i => texTarget(i));
  drawGrid(540, 120, "current texture", i => state.tex[i]);
  for (let i = 0; i < 64; i++) { const e = state.tex[i] - texTarget(i); loss += e * e; }
  state.texLoss = loss / 64;
  drawLabel("each texture cell moves toward the color that lowers residual error", 26, 34);
}

function drawMotion() {
  const poseA = [-0.8, 1.1, -0.9, 0.7, -0.2];
  const poseB = [0.7, -0.7, 0.9, -1.0, 0.55];
  const angles = poseA.map((a, i) => lerp(a, poseB[i], controls.blend));
  drawSkeleton(300, 185, angles, [80, 78, 70, 62, 54], "#0f766e");
  drawSkeleton(640, 185, angles, [80, 78, 70, 62, 54].map(v => v * controls.scale), "#9a3412", controls.constraint);
  const footA = skeletonEnd(300, 185, angles, [80, 78, 70, 62, 54]);
  const footB = skeletonEnd(640, 185, angles, [80, 78, 70, 62, 54].map(v => v * controls.scale));
  state.footSlide = Math.abs((footB.y - 185) / controls.scale - (footA.y - 185)) * (1 - controls.constraint);
  drawLabel("same joint angles, different body scale; constraints reduce foot sliding", 26, 34);
}

function drawLabel(text, x, y) {
  ctx.fillStyle = "rgba(255,255,255,0.86)";
  ctx.fillRect(x - 8, y - 22, Math.min(900, text.length * 7.2 + 16), 34);
  ctx.fillStyle = "#17202a";
  ctx.font = "16px system-ui, sans-serif";
  ctx.fillText(text, x, y);
}

function fillBlock(img, w, x, y, s, r, g, b) {
  for (let yy = 0; yy < s; yy++) for (let xx = 0; xx < s; xx++) {
    const i = ((y + yy) * w + x + xx) * 4;
    img.data[i] = clamp(r, 0, 255); img.data[i + 1] = clamp(g, 0, 255); img.data[i + 2] = clamp(b, 0, 255); img.data[i + 3] = 255;
  }
}

function smoothCircle(x, y, r, blur) {
  return clamp((r - hypot(x, y)) / blur + 0.5, 0, 1);
}

function polygon(pts, stroke, width, fill) {
  ctx.beginPath(); ctx.moveTo(pts[0].x, pts[0].y);
  for (const p of pts.slice(1)) ctx.lineTo(p.x, p.y);
  ctx.closePath(); ctx.fillStyle = fill; ctx.fill(); ctx.strokeStyle = stroke; ctx.lineWidth = width; ctx.stroke();
}

function polyArea(pts) {
  let a = 0;
  for (let i = 0; i < pts.length; i++) {
    const p = pts[i], q = pts[(i + 1) % pts.length];
    a += p.x * q.y - q.x * p.y;
  }
  return Math.abs(a) / 2;
}

function roughness(pts) {
  let r = 0;
  for (let i = 0; i < pts.length; i++) {
    const a = pts[(i + pts.length - 1) % pts.length], p = pts[i], b = pts[(i + 1) % pts.length];
    r += hypot(p.x - (a.x + b.x) / 2, p.y - (a.y + b.y) / 2);
  }
  return r / pts.length;
}

function solveSpring(a, b, rest, k) {
  const dx = b.x - a.x, dy = b.y - a.y, d = hypot(dx, dy) || 1;
  const diff = (d - rest) / d * k;
  if (!a.pin) { a.x += dx * diff * 0.5; a.y += dy * diff * 0.5; }
  if (!b.pin) { b.x -= dx * diff * 0.5; b.y -= dy * diff * 0.5; }
}

function line(a, b) {
  ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
}

function project(p, camX, yaw, f, ox, oy) {
  const x0 = p[0] - camX, y0 = p[1], z0 = p[2];
  const x = x0 * Math.cos(yaw) - z0 * Math.sin(yaw);
  const z = x0 * Math.sin(yaw) + z0 * Math.cos(yaw) + 2.5;
  return { x: ox + x / z * f * 220, y: oy + y0 / z * f * 220 };
}

function drawEdges(pts, edges, color) {
  ctx.strokeStyle = color; ctx.lineWidth = 3;
  for (const [a, b] of edges) line(pts[a], pts[b]);
  ctx.fillStyle = color;
  for (const p of pts) { ctx.beginPath(); ctx.arc(p.x, p.y, 5, 0, TAU); ctx.fill(); }
}

function drawGrid(x0, y0, label, valueFn) {
  ctx.fillStyle = "#17202a"; ctx.font = "16px system-ui, sans-serif"; ctx.fillText(label, x0, y0 - 18);
  const s = 42;
  for (let y = 0; y < 8; y++) for (let x = 0; x < 8; x++) {
    const v = clamp(valueFn(y * 8 + x), 0, 1);
    const c = Math.round(v * 220 + 20);
    ctx.fillStyle = `rgb(${c},${Math.round(c * 0.9)},${Math.round(255 - c * 0.45)})`;
    ctx.fillRect(x0 + x * s, y0 + y * s, s - 2, s - 2);
  }
}

function drawSkeleton(x, y, angles, lengths, color, constraint = 1) {
  let a = Math.PI / 2, px = x, py = y;
  ctx.strokeStyle = color; ctx.lineWidth = 9; ctx.lineCap = "round";
  ctx.fillStyle = color;
  ctx.beginPath(); ctx.arc(px, py, 10, 0, TAU); ctx.fill();
  for (let i = 0; i < angles.length; i++) {
    a += angles[i] * (i % 2 ? -0.55 : 0.55);
    const nx = px + Math.cos(a) * lengths[i];
    let ny = py + Math.sin(a) * lengths[i];
    if (i === angles.length - 1 && constraint > 0.5) ny = Math.min(ny, 620);
    ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(nx, ny); ctx.stroke();
    ctx.beginPath(); ctx.arc(nx, ny, 8, 0, TAU); ctx.fill();
    px = nx; py = ny;
  }
}

function skeletonEnd(x, y, angles, lengths) {
  let a = Math.PI / 2, px = x, py = y;
  for (let i = 0; i < angles.length; i++) {
    a += angles[i] * (i % 2 ? -0.55 : 0.55);
    px += Math.cos(a) * lengths[i]; py += Math.sin(a) * lengths[i];
  }
  return { x: px, y: py };
}

setup();
