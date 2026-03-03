<script lang="ts">
  import { onMount, onDestroy } from "svelte";

  export let idleSeconds = 10; // stop counting after this much inactivity
  export let float = true;     // float bottom-right
  export let compact = true;   // start collapsed

  // Optional: if you want to track only a specific element, pass it in
  // Example usage: <WritingTimer bind:trackEl={textareaEl} />
  export let trackEl: HTMLElement | null = null;

  const STORAGE_KEY = "ll_writing_timer_v1";

  type TimerState = {
    accumulatedMs: number;
    running: boolean;
    lastTickAt: number | null;
    lastInputAt: number | null;
  };

  let state: TimerState = {
    accumulatedMs: 0,
    running: false,
    lastTickAt: null,
    lastInputAt: null
  };

  let ticker: number | null = null;
  let idleChecker: number | null = null;

  // UI
  let isCompact = compact;

  function isHardReload(): boolean {
    try {
      const nav = performance.getEntriesByType("navigation")[0] as PerformanceNavigationTiming | undefined;
      return nav?.type === "reload";
    } catch {
      return false;
    }
  }

  function loadState() {
    // Per your spec: do NOT continue if the page was refreshed
    if (isHardReload()) {
      localStorage.removeItem(STORAGE_KEY);
      return;
    }

    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return;

    try {
      const parsed = JSON.parse(raw) as Partial<TimerState>;
      state = {
        accumulatedMs: Number(parsed.accumulatedMs ?? 0),
        running: Boolean(parsed.running ?? false),
        lastTickAt: parsed.lastTickAt ? Number(parsed.lastTickAt) : null,
        lastInputAt: parsed.lastInputAt ? Number(parsed.lastInputAt) : null
      };

      // If it was running, we resume cleanly (no time is added retroactively).
      // Counting continues only when typing resumes.
      state.running = false;
      state.lastTickAt = null;
    } catch {
      // Corrupt storage; reset safely
      localStorage.removeItem(STORAGE_KEY);
    }
  }

  function saveState() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    let secs = Math.ceil(state.accumulatedMs / 1000);
    let remainder = state.accumulatedMs % 1000;
    // console.log(`the secs are ${secs}s`);
    // console.log(`the remainder are ${remainder}s`);
  }

  function start() {
    if (state.running) return;

    const now = Date.now();
    state.running = true;
    state.lastTickAt = now;

    saveState();
  }

  function stop() {
    if (!state.running) return;

    const now = Date.now();
    let addedMs = 0;
    if (state.lastTickAt) {
      addedMs = Math.max(0, now - state.lastTickAt);
      state.accumulatedMs += addedMs;
    }

    state.running = false;
    state.lastTickAt = null;

    saveState();

    const sessionSecs = Math.ceil(state.accumulatedMs / 1000);
    if (sessionSecs > 0) {
      sendSessionSecs(sessionSecs);
    }
  }

  async function sendSessionSecs(secs: number) {
    try {
      const token = localStorage.getItem('access_token') || localStorage.getItem('token');
      const headers: any = { 'Content-Type': 'application/json' };
      if (token) headers['Authorization'] = `Bearer ${token}`;

      const res = await fetch('http://localhost:8000/api/lyric-tools/save-writing-seconds', {
        method: 'POST',
        credentials: 'include',
        headers:{
            "Content-Type": "application/json"
          },
        body: JSON.stringify({ secs }),
      });

      if (!res.ok) {
        console.warn('Failed to save writing seconds', await res.text());
      }
    } catch (err) {
      console.warn('Error saving writing seconds', err);
    }
  }

  function onUserActivity() {
    const now = Date.now();
    state.lastInputAt = now;

    // Start timer on first activity, and keep it alive while user continues
    if (!state.running) start();

    saveState();
  }

  function tick() {
    if (!state.running || !state.lastTickAt) return;

    const now = Date.now();
    const delta = Math.max(0, now - state.lastTickAt);
    state.accumulatedMs += delta;
    state.lastTickAt = now;

    saveState();
  }

  function checkIdle() {
    if (!state.running) return;
    if (!state.lastInputAt) return;

    const now = Date.now();
    const idleMs = now - state.lastInputAt;

    if (idleMs >= idleSeconds * 1000) {
      stop();

    }
  }

  function format(ms: number) {
    const totalSeconds = Math.floor(ms / 1000);
    const h = Math.floor(totalSeconds / 3600);
    const m = Math.floor((totalSeconds % 3600) / 60);
    const s = totalSeconds % 60;

    const pad = (n: number) => String(n).padStart(2, "0");
    return h > 0 ? `${h}:${pad(m)}:${pad(s)}` : `${m}:${pad(s)}`;
  }

  function bindEvents(el: HTMLElement | Window) {
    // Use a spread of events to catch real “writing” behavior
    const handler = () => onUserActivity();

    // Keyboard + input + paste + IME composition updates
    el.addEventListener("keydown", handler as any);
    el.addEventListener("input", handler as any);
    el.addEventListener("paste", handler as any);
    el.addEventListener("compositionupdate", handler as any);

    return () => {
      el.removeEventListener("keydown", handler as any);
      el.removeEventListener("input", handler as any);
      el.removeEventListener("paste", handler as any);
      el.removeEventListener("compositionupdate", handler as any);
    };
  }

  let unbind: null | (() => void) = null;

  onMount(() => {
    loadState();

    const target: any = trackEl ?? window;
    unbind = bindEvents(target);

    // Run timer tick + idle checker
    ticker = window.setInterval(tick, 1000);
    idleChecker = window.setInterval(checkIdle, 500);

    // Optional: if tab becomes hidden, stop (prevents weird counting when idle)
    const onVis = () => {
      if (document.hidden) stop();
    };
    document.addEventListener("visibilitychange", onVis);

    return () => {
      document.removeEventListener("visibilitychange", onVis);
    };
  });

  onDestroy(() => {
    if (unbind) unbind();
    if (ticker) window.clearInterval(ticker);
    if (idleChecker) window.clearInterval(idleChecker);
  });
</script>

<div class:float-wrap={float} class:compact={isCompact}>
  <button class="timer" on:click={() => (isCompact = !isCompact)} type="button">
    <span class="time">{format(state.accumulatedMs)}</span>
    <span class="status">{state.running ? "Writing" : "Paused"}</span>
  </button>

  {#if !isCompact}
    <div class="panel">
      <div class="row">
        <span>Idle stop:</span>
        <span>{idleSeconds}s</span>
      </div>
      <div class="row">
        <span>Total:</span>
        <span>{format(state.accumulatedMs)}</span>
      </div>
      <div class="actions">
        <button type="button" on:click={stop} disabled={!state.running}>Pause</button>
        <button type="button" on:click={start} disabled={state.running}>Resume</button>
        <button
          type="button"
          on:click={() => {
            state = { accumulatedMs: 0, running: false, lastTickAt: null, lastInputAt: null };
            saveState();
          }}
        >
          Reset
        </button>
      </div>
    </div>
  {/if}
</div>

<style>
  .float-wrap {
    position: fixed;
    right: 16px;
    bottom: 16px;
    z-index: 9999;
  }

  .timer {
    display: flex;
    align-items: baseline;
    gap: 10px;
    padding: 10px 12px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(10,10,10,0.72);
    color: rgba(255,255,255,0.92);
    backdrop-filter: blur(10px);
    cursor: pointer;
  }

  .time {
    font-variant-numeric: tabular-nums;
    font-size: 14px;
    font-weight: 600;
  }

  .status {
    font-size: 12px;
    opacity: 0.7;
  }

  .panel {
    margin-top: 8px;
    padding: 10px 12px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(10,10,10,0.72);
    color: rgba(255,255,255,0.92);
    backdrop-filter: blur(10px);
    min-width: 220px;
  }

  .row {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    font-size: 12px;
    opacity: 0.9;
    margin-bottom: 8px;
  }

  .actions {
    display: flex;
    gap: 8px;
    justify-content: flex-end;
  }

  .actions button {
    padding: 6px 10px;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.10);
    background: rgba(255,255,255,0.04);
    color: rgba(255,255,255,0.92);
    cursor: pointer;
    font-size: 12px;
  }

  .actions button:disabled {
    opacity: 0.45;
    cursor: not-allowed;
  }
</style>