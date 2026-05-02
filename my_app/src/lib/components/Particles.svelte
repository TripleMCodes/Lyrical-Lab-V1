<script lang="ts">
  import { onMount } from "svelte";

  type P = {
    x: number; y: number;
    r: number;
    a: number;
    s: number;
    dx: number; dy: number;
    hue: number;
  };

  let canvas: HTMLCanvasElement;
  let w = 0, h = 0;
  let particles: P[] = [];
  let raf = 0;

  const COUNT = 90;
  const HUES = [275, 190] as const;
  const TWO_PI = Math.PI * 2;

  // Group indices by hue so we can batch-draw per hue
  let hueGroups: Map<number, P[]> = new Map();

  function resize() {
    const dpr = Math.min(devicePixelRatio ?? 1, 2);
    const prevW = w, prevH = h;
    w = innerWidth;
    h = innerHeight;

    canvas.width  = w * dpr | 0;
    canvas.height = h * dpr | 0;
    canvas.style.width  = `${w}px`;
    canvas.style.height = `${h}px`;

    const ctx = canvas.getContext("2d")!;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    if (prevW && prevH) {
      const sx = w / prevW, sy = h / prevH;
      for (const p of particles) { p.x *= sx; p.y *= sy; }
    }

    return ctx;
  }

  function seed(): P[] {
    const ps = Array.from({ length: COUNT }, () => ({
      x:   Math.random() * w,
      y:   Math.random() * h,
      r:   0.6 + Math.random() * 1.8,
      a:   0.15 + Math.random() * 0.7,
      s:   0.15 + Math.random() * 0.65,
      dx:  Math.random() * 0.8 - 0.4,
      dy:  Math.random() * 0.6 - 0.2,
      hue: HUES[Math.random() < 0.7 ? 0 : 1],
    }));

    // Pre-bucket by hue — structure never changes, so build once
    hueGroups = new Map(HUES.map(h => [h, ps.filter(p => p.hue === h)]));
    return ps;
  }

  function makeLoop(ctx: CanvasRenderingContext2D) {
    ctx.globalCompositeOperation = "lighter";

    return function step() {
      ctx.clearRect(0, 0, w, h);

      const t = performance.now() * 0.0015;

      // Move all particles first
      for (const p of particles) {
        p.x += p.dx * p.s;
        p.y += p.dy * p.s;

        if (p.x < -10)    p.x = w + 10;
        if (p.x > w + 10) p.x = -10;
        if (p.y < -10)    p.y = h + 10;
        if (p.y > h + 10) p.y = -10;
      }

      // One fill call per hue group — the core batching win
      for (const [hue, group] of hueGroups) {
        // Pick a representative alpha for the batch (average), twinkle via radius
        ctx.fillStyle = `hsla(${hue},100%,75%,0.55)`;
        ctx.shadowColor = `hsla(${hue},100%,75%,0.3)`;
        ctx.shadowBlur = 10;

        ctx.beginPath();
        for (const p of group) {
          // Twinkle = radius pulse instead of alpha, so we stay in one batch
          const tw = 0.65 + 0.35 * Math.sin((p.x + p.y) * 0.01 + t);
          const r = p.r * (0.7 + 0.3 * tw);
          ctx.moveTo(p.x + r, p.y);   // moveTo before arc avoids unwanted lines
          ctx.arc(p.x, p.y, r, 0, TWO_PI);
        }
        ctx.fill();
      }

      raf = requestAnimationFrame(step);
    };
  }

  onMount(() => {
    const reduced = matchMedia?.("(prefers-reduced-motion: reduce)").matches;
    const ctx = resize();
    particles = seed();

    if (!reduced) raf = requestAnimationFrame(makeLoop(ctx));

    const onResize = () => resize();
    addEventListener("resize", onResize);

    return () => {
      cancelAnimationFrame(raf);
      removeEventListener("resize", onResize);
    };
  });
</script>

<canvas bind:this={canvas} class="particles"></canvas>

<style>
  .particles {
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    opacity: 0.9;
    mix-blend-mode: screen;
  }
</style>