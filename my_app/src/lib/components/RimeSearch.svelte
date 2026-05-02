<script lang="ts">
    import SigilSpinner from '$lib/components/SigilSpinner.svelte';
  import Tooltip from './Tooltip.svelte';

    let {rhyme = $bindable(), rime_list = $bindable(), phraseList = $bindable(), isLoading = $bindable() , findRhyme} = $props();

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
      <button class="mini-rhyme__btn" type="button" onclick={findRhyme}>
        <Tooltip text="Find rhyme">
                <img src="/icons8-find-64.png" alt="search icon" width="50" height="50">
        </Tooltip>
      </button>
    </div>

    <div class="mini-rhyme__results">
      {#if isLoading}
        <SigilSpinner></SigilSpinner>
        <button onclick={() => isLoading = false}>Cancel</button>
      {/if}

      {#if rime_list.length > 0}
        <ul id="results-list" class="results-list">
          {#if phraseList.length > 0}
            {#each phraseList as lst (lst.phrase)}
                  <li>{lst.phrase}</li>
            {/each}
          {/if}
          {#each rime_list as rime (rime.word)}
            <li>{rime.word}</li>

          {/each}
        </ul>
      {:else if isLoading === false}
        <p class="mini-rhyme__empty">No results</p>
      {/if}

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
  background-color: transparent;
  border-color: transparent;
  border-radius: 999px;
  padding: 0.5rem 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.mini-rhyme__btn:hover {
  box-shadow: 0 0 14px rgba(168, 85, 247, 0.28);
  border-color: transparent;
  background-color: transparent;
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


.mini-rhyme__results{
  overflow-y: scroll;
  display: flex;
  flex-direction: column;
}

.mini-rhyme__results{
  scrollbar-width: thin;
  scrollbar-color: transparent transparent;
}

.mini-rhyme__results::-webkit-scrollbar {
  width: 2%;
}

.mini-rhyme__results::-webkit-scrollbar-track {
  background: transparent;
}

.mini-rhyme__results:hover::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.15);
}

/* Container styling */
#results-list {
  list-style: none;
  padding: 0;
  margin: 1rem 0;
  background-color: #1a0a2b; /* very dark purple */
  border-radius: 12px;
  box-shadow: 0 0 20px rgba(128, 0, 255, 0.4); /* soft neon glow */
  max-height: 400px;
  overflow-y: scroll;
  overflow-x: hidden;
  
}

/* Inner UL */
#results-list ul {
  padding: 0;
  margin: 0;
}

/* Each result item */
#results-list li, .notify {
  padding: 0.8rem 1rem;
  border-bottom: 1px solid rgba(128, 0, 255, 0.2);
  color: #d8b3ff; /* light neon purple */
  font-family: 'Fira Mono', monospace;
  font-weight: 500;
  transition: all 0.2s ease-in-out;
  cursor: pointer;
}

/* Hover glow effect */
#results-list li:hover, .notify {
  background-color: rgba(128, 0, 255, 0.2);
  text-shadow: 0 0 10px #d8b3ff;
  transform: translateX(5px);
}

/* Last item: no border */
#results-list li:last-child {
  border-bottom: none;
}


/* =========================================
   MEDIA QUERIES — Rhyme Search Component
   xs: < 375px  |  sm: 375–639px  |  md: 640–1023px
   lg: 1024–1279px  |  xl: 1280+  |  2xl: 1600+
   ========================================= */

/* -----------------------------------------
   XS — Very small phones (< 375px)
   ----------------------------------------- */
@media (max-width: 374px) {
  .sider-items {
    gap: 0.6rem;
  }

  .mini-rhyme {
    padding: 0.75rem 0.875rem;
    border-radius: 12px;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
  }

  .mini-rhyme h4 {
    font-size: 0.68rem;
    margin-bottom: 0.5rem;
  }

  .mini-rhyme__bar {
    gap: 0.4rem;
    flex-direction: column;
  }

  .mini-rhyme__input {
    font-size: 0.78rem;
    padding: 0.45rem 0.6rem;
    border-radius: 10px;

  }

  .mini-rhyme__btn {
    padding: 0.3rem 0.5rem;
  }

  /* Shrink icon — 50px is too large on xs */
  .mini-rhyme__btn img {
    width: 32px;
    height: 32px;
  }

  .mini-rhyme__results {
    margin-top: 0.5rem;
    padding: 0.55rem 0.65rem;
    border-radius: 10px;
    min-height: 56px;
  }

  .mini-rhyme__empty {
    font-size: 0.75rem;
  }

  /* Results list */
  #results-list {
    max-height: 200px;        /* Much shorter — xs screens are shallow */
    border-radius: 8px;
    margin: 0.5rem 0;
  }

  #results-list li,
  .notify {
    padding: 0.55rem 0.75rem;
    font-size: 0.78rem;
  }

  #results-list li:hover {
    transform: translateX(3px); /* Reduce slide — less jarring on touch */
  }
}

/* -----------------------------------------
   SM — Standard phones (375px – 639px)
   ----------------------------------------- */
@media (min-width: 375px) and (max-width: 639px) {
  .sider-items {
    gap: 0.75rem;
  }

  .mini-rhyme {
    padding: 0.875rem 1rem;
    border-radius: 13px;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
  }

  .mini-rhyme h4 {
    font-size: 0.72rem;
    margin-bottom: 0.5rem;
  }

  .mini-rhyme__bar {
    gap: 0.5rem;
    flex-direction: column;
  }

  .mini-rhyme__input {
    font-size: 0.82rem;
    padding: 0.5rem 0.65rem;
    border-radius: 10px;
  }

  .mini-rhyme__btn {
    padding: 0.35rem 0.6rem;
  }

  .mini-rhyme__btn img {
    width: 36px;
    height: 36px;
  }

  .mini-rhyme__results {
    margin-top: 0.6rem;
    padding: 0.6rem 0.75rem;
    border-radius: 10px;
    min-height: 60px;
  }

  .mini-rhyme__empty {
    font-size: 0.78rem;
  }

  #results-list {
    max-height: 240px;
    border-radius: 10px;
    margin: 0.65rem 0;
  }

  #results-list li,
  .notify {
    padding: 0.65rem 0.875rem;
    font-size: 0.82rem;
  }

  #results-list li:hover {
    transform: translateX(3px);
  }
}

/* -----------------------------------------
   MD — Large phones / small tablets (640px – 1023px)
   ----------------------------------------- */
@media (min-width: 640px) and (max-width: 1023px) {
  .sider-items {
    gap: 0.875rem;
  }

  .mini-rhyme {
    padding: 0.875rem 1rem;
    border-radius: 14px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
  }

  .mini-rhyme h4 {
    font-size: 0.74rem;
    margin-bottom: 0.5rem;
  }

  .mini-rhyme__input {
    font-size: 0.83rem;
    padding: 0.52rem 0.7rem;
  }

  .mini-rhyme__btn img {
    width: 40px;
    height: 40px;
  }

  .mini-rhyme__results {
    min-height: 64px;
    border-radius: 11px;
  }

  #results-list {
    max-height: 280px;
    border-radius: 10px;
  }

  #results-list li,
  .notify {
    padding: 0.7rem 0.9rem;
    font-size: 0.84rem;
  }
}

/* -----------------------------------------
   LG — Tablets / small laptops (1024px – 1279px)
   ----------------------------------------- */
@media (min-width: 1024px) and (max-width: 1279px) {
  .mini-rhyme {
    padding: 0.9rem 1rem;
    border-radius: 15px;
    backdrop-filter: blur(13px);
    -webkit-backdrop-filter: blur(13px);
  }

  .mini-rhyme h4 {
    font-size: 0.75rem;
  }

  .mini-rhyme__input {
    font-size: 0.84rem;
  }

  .mini-rhyme__btn img {
    width: 44px;
    height: 44px;
  }

  .mini-rhyme__results {
    min-height: 68px;
  }

  #results-list {
    max-height: 320px;
  }

  #results-list li,
  .notify {
    padding: 0.72rem 0.9rem;
    font-size: 0.85rem;
  }
}

/* -----------------------------------------
   XL — Standard desktops (1280px – 1599px)
   ----------------------------------------- */
@media (min-width: 1280px) {
  /* Base styles are tuned for this range — preserved.
     padding: 1rem, border-radius: 16px,
     max-height: 400px, icon: 50px are all intentional. */

  .mini-rhyme__btn img {
    width: 50px;              /* Matches base */
    height: 50px;
  }

  #results-list {
    max-height: 400px;        /* Matches base */
  }
}

/* -----------------------------------------
   2XL — Large / wide monitors (1600px+)
   ----------------------------------------- */
@media (min-width: 1600px) {
  .sider-items {
    gap: 1.25rem;
  }

  .mini-rhyme {
    padding: 1.25rem 1.4rem;
    border-radius: 20px;
  }

  .mini-rhyme h4 {
    font-size: 0.85rem;
    margin-bottom: 0.75rem;
  }

  .mini-rhyme__bar {
    gap: 0.75rem;
  }

  .mini-rhyme__input {
    font-size: 0.9rem;
    padding: 0.65rem 0.875rem;
    border-radius: 14px;
  }

  .mini-rhyme__btn {
    padding: 0.6rem 1rem;
  }

  .mini-rhyme__btn img {
    width: 56px;
    height: 56px;
  }

  .mini-rhyme__results {
    margin-top: 0.9rem;
    padding: 0.9rem 1rem;
    border-radius: 14px;
    min-height: 80px;
  }

  .mini-rhyme__empty {
    font-size: 0.88rem;
  }

  #results-list {
    max-height: 460px;
    border-radius: 14px;
    margin: 1rem 0;
  }

  #results-list li,
  .notify {
    padding: 0.9rem 1.1rem;
    font-size: 0.9rem;
  }
}

</style>
