<script lang="ts">
  import { onMount } from "svelte";

  type P = {
    x: number; y: number;
    r: number;
    a: number;   // alpha
    s: number;   // speed
    dx: number; dy: number;
    hue: number;
  };

  let canvas: HTMLCanvasElement;
  let ctx: CanvasRenderingContext2D | null = null;
  let w = 0, h = 0;
  let particles: P[] = [];
  let raf = 0;

  const count = 90; // tweak: 60–180 depending on taste

  function resize() {
    w = window.innerWidth;
    h = window.innerHeight;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.floor(w * dpr);
    canvas.height = Math.floor(h * dpr);
    canvas.style.width = `${w}px`;
    canvas.style.height = `${h}px`;
    ctx = canvas.getContext("2d");
    ctx?.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function seed() {
    particles = Array.from({ length: count }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      r: 0.6 + Math.random() * 1.8,
      a: 0.15 + Math.random() * 0.7,
      s: 0.15 + Math.random() * 0.65,
      dx: (-0.4 + Math.random() * 0.8),
      dy: (-0.2 + Math.random() * 0.6),
      hue: Math.random() < 0.7 ? 275 : 190, // mostly purple, some cyan
    }));
  }

  function step() {
    if (!ctx) return;
    ctx.clearRect(0, 0, w, h);

    // subtle glow wash
    ctx.globalCompositeOperation = "lighter";

    for (const p of particles) {
      p.x += p.dx * p.s;
      p.y += p.dy * p.s;

      // wrap around edges
      if (p.x < -10) p.x = w + 10;
      if (p.x > w + 10) p.x = -10;
      if (p.y < -10) p.y = h + 10;
      if (p.y > h + 10) p.y = -10;

      // twinkle
      const tw = 0.65 + 0.35 * Math.sin((p.x + p.y) * 0.01 + performance.now() * 0.0015);

      ctx.beginPath();
      ctx.fillStyle = `hsla(${p.hue}, 100%, 75%, ${p.a * tw})`;
      ctx.shadowBlur = 12;
      ctx.shadowColor = `hsla(${p.hue}, 100%, 75%, 0.35)`;
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.globalCompositeOperation = "source-over";
    raf = requestAnimationFrame(step);
  }

  onMount(() => {
    // reduced motion check
    const reduced = window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches;
    resize();
    seed();
    if (!reduced) step();

    window.addEventListener("resize", () => { resize(); seed(); });

    return () => cancelAnimationFrame(raf);
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
