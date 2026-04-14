<script>
  import Tooltip from "./Tooltip.svelte";
  import { searchLyrics } from "$lib/api/lyric_tools";

  let {display = $bindable(), results = $bindable(), openSong} = $props()

  let searchQuery = $state("");
  let isLoading = $state(false);
  let error = $state("");

  async function performSearch() {
    if (!searchQuery.trim()) {
      error = "Please enter a search query";
      return;
    }

    isLoading = true;
    error = "";

    try {
      const response = await searchLyrics(searchQuery.trim(), 10);
      results = response.results || [];
      display = true;
    } catch (err) {
      error = err.message || "Search failed";
      results = [];
      display = false;
    } finally {
      isLoading = false;
    }
  }

  function handleKeyPress(event) {
    if (event.key === 'Enter') {
      performSearch();
    }
  }

  function clearSearch() {
    searchQuery = "";
    results = [];
    display = false;
    error = "";
  }

</script>

<section class="song-search">
  <div class="search-bar">
    <input
      type="text"
      name="song-search"
      class="search-input"
      placeholder="Search songs… (title, artist, album)"
      bind:value={searchQuery}
      onkeypress={handleKeyPress}
      disabled={isLoading}
    />
    <button class="search-btn" type="button" onclick={performSearch} disabled={isLoading || !searchQuery.trim()}>
      <Tooltip text="Search for song">
        {#if isLoading}
          <div class="spinner"></div>
        {:else}
          <img src="/icons8-find-64.png" alt="search icon" width="50" height="50">
        {/if}
      </Tooltip>
    </button>
    {#if searchQuery}
      <button class="clear-btn" type="button" onclick={clearSearch} title="Clear search">
        ✕
      </button>
    {/if}
  </div>

  {#if error}
    <div class="error-message">
      {error}
    </div>
  {/if}
</section>

<section class="display-results">
  {#if display && results?.length}
    <div class="results-grid">
      {#each results as song}
        <div class="result-card">
          <div class="result-meta">
            <p class="meta-line"><span class="meta-label">Artist</span>{song.artist || 'Unknown'}</p>
            <p class="meta-line"><span class="meta-label">Title</span>{song.title || 'Untitled'}</p>
            {#if song.album}
              <p class="meta-line"><span class="meta-label">Album</span>{song.album}</p>
            {/if}
            <p class="meta-line"><span class="meta-label">Score</span>{song.score?.toFixed(3) || 'N/A'}</p>
          </div>

          {#if song.snippet}
            <div class="snippet">
              <p class="snippet-text">"{song.snippet}"</p>
            </div>
          {/if}

          <button class="open-btn" type="button" onclick={() => openSong(song)}>Open in studio</button>
        </div>
      {/each}
    </div>
  {:else if display && !isLoading}
    <p class="empty">No results found for "{searchQuery}"</p>
  {:else if !display && !isLoading}
    <p class="empty">Search your lyrics to get started</p>
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

.search-btn button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Clear button */
.clear-btn {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 30px;
  height: 30px;
  margin-top: 5px;
  padding: 5px;
  border-radius: 50%;
  border: 1px solid rgba(168, 85, 247, 0.3);
  background: rgba(168, 85, 247, 0.1);
  color: rgba(245, 233, 255, 0.8);
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-btn:hover {
  background: rgba(168, 85, 247, 0.2);
  border-color: rgba(168, 85, 247, 0.5);
}

/* Spinner */
.spinner {
  width: 24px;
  height: 24px;
  border: 2px solid rgba(168, 85, 247, 0.3);
  border-top: 2px solid rgba(168, 85, 247, 0.8);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Error message */
.error-message {
  margin-top: 0.5rem;
  padding: 0.75rem;
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid rgba(220, 53, 69, 0.3);
  border-radius: 8px;
  color: rgba(255, 193, 193, 0.9);
  font-size: 0.9rem;
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

/* Snippet */
.snippet {
  margin-top: 0.5rem;
  padding: 0.75rem;
  background: rgba(15, 5, 25, 0.4);
  border-radius: 8px;
  border-left: 3px solid rgba(168, 85, 247, 0.5);
}

.snippet-text {
  margin: 0;
  font-size: 0.85rem;
  color: rgba(233, 213, 255, 0.8);
  font-style: italic;
  line-height: 1.4;
}

/* Empty state */
.empty {
  margin: 0.6rem 0;
  color: rgba(233, 213, 255, 0.6);
  font-size: 0.9rem;
}

</style>