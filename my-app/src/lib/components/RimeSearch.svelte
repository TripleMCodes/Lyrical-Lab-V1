<script lang="ts">
    let {rhyme = $bindable(), rime_list = $bindable()} = $props();
</script>
<section class="sider-items">
  <div class="mini-rhyme">
    <h4>Rhyme Preview</h4>

    <div class="mini-rhyme__bar">
      <input
        class="mini-rhyme__input"
        type="text"
        bind:value={rhyme}
        placeholder="Type a word…"
      />
      <button class="mini-rhyme__btn" type="button">Go</button>
    </div>

    <div class="mini-rhyme__results">
      <!-- results render here later -->
      <p class="mini-rhyme__empty">No results yet</p>
    </div>
  </div>
</section>

<style>
/* Container */
.sider-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: none;
}

/* Mini card */
.mini-rhyme {
  background: linear-gradient(
    180deg,
    rgba(120, 50, 180, 0.22),
    rgba(30, 10, 45, 0.62)
  );

  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);

  border: 1px solid rgba(168, 85, 247, 0.22);
  border-radius: 16px;

  padding: 1rem 1rem;

  box-shadow:
    0 0 22px rgba(168, 85, 247, 0.12),
    inset 0 0 0 1px rgba(255, 255, 255, 0.03);

  color: rgba(245, 233, 255, 0.95);
}

/* Title */
.mini-rhyme h4 {
  margin:0;

  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;

  color: rgba(233, 213, 255, 0.75);
}

/* Input + button row */
.mini-rhyme__bar {
  display: flex;
  gap: 0.6rem;
  align-items: center;
}

/* Input */
.mini-rhyme__input {
  flex: 1;

  background: rgba(15, 5, 25, 0.6);
  border: 1px solid rgba(168, 85, 247, 0.18);
  border-radius: 12px;

  padding: 0.55rem 0.75rem;

  color: rgba(245, 233, 255, 0.95);
  font-size: 0.85rem;

  outline: none;
}

.mini-rhyme__input::placeholder {
  color: rgba(233, 213, 255, 0.45);
}

.mini-rhyme__input:focus {
  border-color: rgba(168, 85, 247, 0.45);
  box-shadow: 0 0 12px rgba(168, 85, 247, 0.22);
}

/* Button */
.mini-rhyme__btn {
  background: rgba(168, 85, 247, 0.16);
  border: 1px solid rgba(168, 85, 247, 0.34);
  border-radius: 999px;

  padding: 0.5rem 0.85rem;

  color: rgba(245, 233, 255, 0.95);
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;

  cursor: pointer;
  transition: all 0.2s ease;
}

.mini-rhyme__btn:hover {
  background: rgba(168, 85, 247, 0.26);
  box-shadow: 0 0 14px rgba(168, 85, 247, 0.28);
}

/* Results area */
.mini-rhyme__results {
  margin-top: 0.75rem;

  padding: 0.75rem 0.85rem;

  background: rgba(10, 3, 16, 0.35);
  border: 1px solid rgba(168, 85, 247, 0.12);
  border-radius: 12px;

  min-height: 72px;

  overflow: hidden;
}

/* Empty text */
.mini-rhyme__empty {
  margin: 0;
  font-size: 0.82rem;
  color: rgba(233, 213, 255, 0.55);
}

/* Placeholder for later sider content */
.sider-slot {
  min-height: 40px;
}
</style>
