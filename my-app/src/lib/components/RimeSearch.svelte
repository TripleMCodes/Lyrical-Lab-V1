<script lang="ts">
    import SigilSpinner from '$lib/components/SigilSpinner.svelte';

    let {rhyme = $bindable(), rime_list = $bindable(), isLoading = $bindable() , findRhyme} = $props();


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
      <button class="mini-rhyme__btn" type="button" onclick={findRhyme}>Go</button>
    </div>

    <div class="mini-rhyme__results">
      {#if isLoading}
        <SigilSpinner></SigilSpinner>
        <button onclick={() => isLoading = false}>Cancel</button>
      {/if}

      {#if rime_list.length > 0}
        <ul id="results-list" class="results-list">
          {#each rime_list as rime (rime.word)}
            <li>{rime.word}</li>
          {/each}
        </ul>
            <!-- <p>{rime.word}</p> -->
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


.mini-rhyme__results{
  height: 100px;
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

button{
  text-align:center;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #c77dff, #7b2cbf);
  color: #fff;
  border: 1px solid rgba(199, 125, 255, 0.6);
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 0 15px rgba(199, 125, 255, 0.4);
  transition: all 0.3s ease;
  font-family: inherit;
}

 button:hover {
    background: linear-gradient(135deg, #e0aaff, #9d4edd);
    box-shadow: 0 0 25px rgba(199, 125, 255, 0.7);
    transform: translateY(-2px);
}

button:active {
    transform: translateY(0);
    box-shadow: 0 0 12px rgba(199, 125, 255, 0.5);
}


/* Container styling */
#results-list {
  list-style: none;
  padding: 0;
  margin: 1rem 0;
  background-color: #1a0a2b; /* very dark purple */
  border-radius: 12px;
  box-shadow: 0 0 20px rgba(128, 0, 255, 0.4); /* soft neon glow */
  /* max-width: 400px; */
  max-height: 400px;
  overflow-y: scroll;
  overflow-x: hidden;
  
}

/* Inner UL (if you want it nested) */
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
