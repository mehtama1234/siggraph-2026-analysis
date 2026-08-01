export function buildAdjacency(vertexCount, edges) {
  const adjacency = Array.from({ length: vertexCount }, () => []);
  for (const [a, b] of edges) {
    adjacency[a].push(b);
    adjacency[b].push(a);
  }
  return adjacency;
}

export function polygonArea(vertices) {
  let area = 0;
  for (let i = 0; i < vertices.length; i++) {
    const p = vertices[i];
    const q = vertices[(i + 1) % vertices.length];
    area += p.x * q.y - q.x * p.y;
  }
  return Math.abs(area) / 2;
}

export function roughness(vertices, edges) {
  const adjacency = buildAdjacency(vertices.length, edges);
  let total = 0;
  for (let i = 0; i < vertices.length; i++) {
    const n = adjacency[i];
    if (!n.length) continue;
    const avg = n.reduce((acc, j) => {
      acc.x += vertices[j].x;
      acc.y += vertices[j].y;
      return acc;
    }, { x: 0, y: 0 });
    avg.x /= n.length;
    avg.y /= n.length;
    total += Math.hypot(vertices[i].x - avg.x, vertices[i].y - avg.y);
  }
  return total / vertices.length;
}

export function smoothMesh(vertices, edges, options = {}) {
  const iterations = options.iterations ?? 10;
  const amount = options.amount ?? 0.35;
  const preserveArea = options.preserveArea ?? 0;
  const locked = new Set(options.locked ?? []);
  const adjacency = buildAdjacency(vertices.length, edges);
  const original = vertices.map((p) => ({ ...p }));
  const originalArea = polygonArea(vertices);
  let current = vertices.map((p) => ({ ...p }));

  for (let it = 0; it < iterations; it++) {
    const next = current.map((p, i) => {
      if (locked.has(i) || adjacency[i].length === 0) return { ...p };
      const avg = adjacency[i].reduce((acc, j) => {
        acc.x += current[j].x;
        acc.y += current[j].y;
        return acc;
      }, { x: 0, y: 0 });
      avg.x /= adjacency[i].length;
      avg.y /= adjacency[i].length;
      return {
        x: p.x + (avg.x - p.x) * amount,
        y: p.y + (avg.y - p.y) * amount
      };
    });
    if (preserveArea > 0) {
      const area = polygonArea(next);
      const scale = area > 0 ? Math.sqrt(originalArea / area) : 1;
      const cx = next.reduce((s, p) => s + p.x, 0) / next.length;
      const cy = next.reduce((s, p) => s + p.y, 0) / next.length;
      for (let i = 0; i < next.length; i++) {
        if (locked.has(i)) continue;
        next[i].x = cx + (next[i].x - cx) * (1 + (scale - 1) * preserveArea);
        next[i].y = cy + (next[i].y - cy) * (1 + (scale - 1) * preserveArea);
      }
    }
    current = next;
  }

  let maxMovement = 0;
  for (let i = 0; i < current.length; i++) {
    maxMovement = Math.max(maxMovement, Math.hypot(current[i].x - original[i].x, current[i].y - original[i].y));
  }

  return {
    vertices: current,
    metrics: {
      roughness: roughness(current, edges),
      originalRoughness: roughness(original, edges),
      areaRatio: polygonArea(current) / originalArea,
      maxMovement
    }
  };
}

export function generateNoisyLoop(count = 36, radius = 1, noise = 0.18) {
  const vertices = [];
  const edges = [];
  for (let i = 0; i < count; i++) {
    const a = i / count * Math.PI * 2;
    const r = radius * (1 + Math.sin(i * 2.1) * noise + Math.cos(i * 4.7) * noise * 0.45);
    vertices.push({ x: Math.cos(a) * r, y: Math.sin(a) * r });
    edges.push([i, (i + 1) % count]);
  }
  return { vertices, edges };
}

