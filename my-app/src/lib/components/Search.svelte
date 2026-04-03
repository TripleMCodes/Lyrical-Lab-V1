<script>
  import Tooltip from "./Tooltip.svelte";


    let {display = $bindable(), results = $bindable() } = $props()

</script>

<section class="song-search">
  <div class="search-bar">
    <input
      type="text"
      name="song-search"
      class="search-input"
      placeholder="Search songs… (title, artist, album)"
    />
    <button class="search-btn" type="button">
      <Tooltip text="Search for song">
                <img src="/icons8-find-64.png" alt="search icon" width="50" height="50">
      </Tooltip>
    </button>
  </div>
</section>

<section class="display-results">
  {#if display && results?.length}
    <div class="results-grid">
      {#each results as song}
        <div class="result-card">
          <div class="result-meta">
            <p class="meta-line"><span class="meta-label">Artist</span>{song.artist}</p>
            <p class="meta-line"><span class="meta-label">Title</span>{song.title}</p>
            {#if song.album}
              <p class="meta-line"><span class="meta-label">Album</span>{song.album}</p>
            {/if}
          </div>

          <button class="open-btn" type="button">Open in studio</button>
        </div>
      {/each}
    </div>
  {:else}
    <p class="empty">No results to display</p>
  {/if}
</section>


<style>
    /* Container */
.song-search {
  width: 100%;
  margin-bottom: 1rem;
}

/* Search bar glass */
.search-bar {
  display: flex;
  gap: 0.75rem;
  align-items: center;

  background: linear-gradient(
    180deg,
    rgba(120, 50, 180, 0.18),
    rgba(30, 10, 45, 0.55)
  );

  border: 1px solid rgba(168, 85, 247, 0.22);
  border-radius: 16px;

  padding: 0.75rem;

  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);

  box-shadow:
    0 0 22px rgba(168, 85, 247, 0.12),
    inset 0 0 0 1px rgba(255, 255, 255, 0.03);
}

/* Input */
.search-input {
  flex: 1;

  background: rgba(15, 5, 25, 0.6);
  border: 1px solid rgba(168, 85, 247, 0.18);
  border-radius: 12px;

  padding: 0.7rem 0.9rem;

  color: rgba(245, 233, 255, 0.95);
  font-size: 0.9rem;

  outline: none;
}

.search-input::placeholder {
  color: rgba(233, 213, 255, 0.45);
}

.search-input:focus {
  border-color: rgba(168, 85, 247, 0.45);
  box-shadow: 0 0 12px rgba(168, 85, 247, 0.22);
}

/* Search button */
.search-btn button, button {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 50px;
  height: 50px;
  margin-top: 5px;
  padding: 7px;
  border-radius: 8px;
  border: none;
  background-color: transparent;
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  }

.search-btn button:hover {
  transform: translateY(-1px);
  box-shadow:
      0 12px 28px rgba(180, 90, 255, 0.45),
      0 0 0 1px rgba(220, 160, 255, 0.5);
}

.search-btn button:active {
  transform: translateY(0);
  box-shadow:
      0 6px 14px rgba(140, 70, 200, 0.4);
  }

/* Results section */
.display-results {
  width: 100%;
}

/* Grid of results */
.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

/* Card */
.result-card {
  background: linear-gradient(
    180deg,
    rgba(120, 50, 180, 0.22),
    rgba(30, 10, 45, 0.62)
  );

  border: 1px solid rgba(168, 85, 247, 0.22);
  border-radius: 18px;

  padding: 1rem 1.1rem;

  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);

  box-shadow:
    0 0 20px rgba(168, 85, 247, 0.12),
    inset 0 0 0 1px rgba(255, 255, 255, 0.03);

  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

/* Meta */
.result-meta {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.meta-line {
  margin: 0;
  font-size: 0.9rem;
  color: rgba(233, 213, 255, 0.9);

  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.meta-label {
  display: inline-block;
  width: 60px;

  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;

  color: rgba(233, 213, 255, 0.55);
}

/* Open button */
.open-btn {
  align-self: flex-start;

  background: rgba(168, 85, 247, 0.14);
  border: 1px solid rgba(168, 85, 247, 0.32);
  border-radius: 12px;

  padding: 0.55rem 0.85rem;

  color: rgba(245, 233, 255, 0.95);
  font-size: 0.75rem;
  font-weight: 600;

  letter-spacing: 0.04em;
  text-transform: uppercase;

  cursor: pointer;
  transition: all 0.2s ease;
}

.open-btn:hover {
  background: rgba(168, 85, 247, 0.24);
  box-shadow: 0 0 14px rgba(168, 85, 247, 0.28);
}

/* Empty state */
.empty {
  margin: 0.6rem 0;
  color: rgba(233, 213, 255, 0.6);
  font-size: 0.9rem;
}

</style>