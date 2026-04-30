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

</style>
