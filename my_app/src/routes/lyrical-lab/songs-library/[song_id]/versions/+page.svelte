<script lang="ts">
  import { goto } from '$app/navigation';
  import type { PageData } from './$types';
  import { writable } from 'svelte/store';
  import { slide } from 'svelte/transition';
  import {get_url} from "$lib/url_vars/urls_vars"

  let { data } = $props<{ data: PageData }>();

  let song = $derived(data.versions.song);
  let song_id = $derived(data.song.song_id);
  let versions = $derived(data.versions.versions);

  // Store for tracking which version cards are open
  const openVersions = writable<number[]>([]);

  const goBack = () => goto('/lyrical-lab/songs-library');

  const toggleVersion = (versionNumber: number) => {
    openVersions.update(current => {
      if (current.includes(versionNumber)) {
        return current.filter(v => v !== versionNumber);
      } else {
        return [...current, versionNumber];
      }
    });
  };

  const delete_song = async () => {
    if (confirm('Are you sure you want to delete this song? This action cannot be undone.')) {
      try {
        const response = await fetch(`${get_url()}/api/songs/${song.id}`, { method: 'DELETE' });
        if (response.ok) goto('/lyrical-lab/songs-library');
        else alert('Failed to delete the song.');
      } catch (err) {
        console.error('Error deleting song:', err);
        alert('An error occurred while deleting the song.');
      }
    }
  };
</script>

<div class="song-detail-container">
  <button class="back-btn" onclick={goBack}>← Back to Library</button>

  {#if versions && versions.length > 0}
    <div class="song-header">
      <h2>{song.song_name}</h2>
      <div class="header-meta">
        <div class="meta-item">
          <span class="label">Artist</span>
          <span class="value">{song.song_artist}</span>
        </div>
        <div class="meta-item">
          <span class="label">Genre</span>
          <span class="value">{song.song_genre}</span>
        </div>
      </div>

      <div class="lyrics-container">
        <h3>Current Version Lyrics</h3>
        <div class="lyrics-text">{song.song_lyrics}</div>
      </div>

      <div class="versions-list">
        <h3>Other Versions</h3>
        {#each versions as version (version.version)}
          <div class="version-card">
            <!-- svelte-ignore a11y_click_events_have_key_events -->
            <!-- svelte-ignore a11y_no_static_element_interactions -->
            <div class="version-header" onclick={() => toggleVersion(version.version)}>
              <h4>Version {version.version}</h4>
              <span class="toggle-icon">
                {#if $openVersions.includes(version.version)}
                  ▼
                {:else}
                  ▶
                {/if}
              </span>
            </div>

            {#if $openVersions.includes(version.version)}
              <div class="version-lyrics" transition:slide={{ duration: 250 }}>
                <div class="lyrics-text">{version.lyrics}</div>
              </div>
            {/if}
          </div>
        {/each}
      </div>
    </div>
  {:else}
    <p class="info">No versions available for this song.</p>
  {/if}

  <div class="actions">
    <button onclick={delete_song}>Delete Song</button>
  </div>
</div>

<style>
  .song-detail-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem 1.5rem;
  }

  .back-btn, button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: linear-gradient(135deg, #c77dff, #7b2cbf);
    color: #fff;
    border: 1px solid rgba(199, 125, 255, 0.6);
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    margin-bottom: 1.5rem;
    box-shadow: 0 0 16px rgba(199, 125, 255, 0.45);
    transition: all 0.25s ease;
  }

  .back-btn:hover, button:hover {
    background: linear-gradient(135deg, #e0aaff, #9d4edd);
    box-shadow: 0 0 26px rgba(199, 125, 255, 0.7);
    transform: translateX(-2px);
  }

  .song-header {
    background: linear-gradient(160deg, #0b0014, #16001f);
    border: 1px solid rgba(199, 125, 255, 0.3);
    border-radius: 16px;
    padding: 2rem;
    box-shadow:
      inset 0 0 14px rgba(180, 120, 255, 0.12),
      0 0 30px rgba(120, 60, 255, 0.25);
    margin-bottom: 2rem;
  }

  .song-header h2 {
    color: #fff;
    font-size: 2rem;
    margin-bottom: 1rem;
    text-shadow: 0 0 15px rgba(199, 125, 255, 0.8);
  }

  .header-meta {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .meta-item .label {
    font-size: 0.75rem;
    color: #a080bf;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 600;
  }

  .meta-item .value {
    font-size: 1rem;
    color: #e6ccff;
    font-weight: 500;
  }

  .lyrics-container {
    background: linear-gradient(160deg, #0b0014, #16001f);
    border: 1px solid rgba(199, 125, 255, 0.3);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow:
      inset 0 0 12px rgba(180, 120, 255, 0.12),
      0 0 20px rgba(120, 60, 255, 0.2);
  }

  .lyrics-text {
    color: #e6ccff;
    font-size: 1rem;
    line-height: 1.6;
    white-space: pre-wrap;
    word-wrap: break-word;
    padding: 1rem;
    border-left: 3px solid rgba(199, 125, 255, 0.35);
    border-radius: 8px;
    background: rgba(199, 125, 255, 0.05);
  }

  .versions-list h3 {
    color: #f2d9ff;
    margin-bottom: 1rem;
  }

  .version-card {
    margin-bottom: 1rem;
    border-radius: 12px;
    overflow: hidden;
    background: rgba(11, 0, 20, 0.7);
    border: 1px solid rgba(199, 125, 255, 0.25);
  }

  .version-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    padding: 1rem;
    background: rgba(199, 125, 255, 0.1);
    transition: background 0.2s ease;
  }

  .version-header:hover {
    background: rgba(199, 125, 255, 0.2);
  }

  .toggle-icon {
    font-weight: bold;
    color: #f2d9ff;
  }

  .version-lyrics {
    padding: 1rem;
    border-top: 1px solid rgba(199, 125, 255, 0.2);
  }

  .actions {
    display: flex;
    gap: 1rem;
  }

  .info {
    color: #e0aaff;
    font-style: italic;
    text-align: center;
    margin-top: 2rem;
  }

  @media (max-width: 768px) {
    .song-detail-container {
      padding: 1rem;
    }
    .song-header {
      padding: 1rem;
    }
    .lyrics-container, .version-card {
      padding: 1rem;
    }
    .lyrics-text {
      font-size: 0.95rem;
      padding: 0.8rem;
    }
  }
</style>