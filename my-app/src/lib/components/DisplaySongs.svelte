<script>
    let {filteredSongs = $bindable(), handleSongClick } = $props()
</script>

<section class="display-songs">
    <h2>Your Songs ({filteredSongs.length})</h2>
    {#if filteredSongs.length > 0}
        <div class="songs-grid">
            {#each filteredSongs as song (song.song_id)}
            <div class="song-card" role="button" tabindex="0" onclick={() => handleSongClick(song.song_id)} onkeydown={(e) => e.key === 'Enter' && handleSongClick(song.song_id)}>
                <div class="song">
                    <h3>{song.song_name}</h3>
                </div>
                <div class="song-details">
                    <p>Artist: <span class="name">{song.song_artist}</span></p>
                    <p>Genre: <span>{song.song_genre}</span></p>
                    {#if song.song_mood}
                    <p>Mood: <span>{song.song_mood}</span></p>
                    {/if}
                    {#if song.song_album}
                    <p>Album: <span>{song.song_album}</span></p>
                    {:else}
                    <p>Album: <span>None</span></p>
                    {/if}
                    <p>Written on: <span>{new Date(song.date_created).toLocaleDateString()}</span></p>
                </div>
                <div class="lyrics">
                    {song.song_lyrics}
                </div>
                <div class="card-overlay">Click to view full lyrics →</div>
            </div>
            {/each}
        </div>
    {:else}
        <p>No songs found matching your filters.</p>
    {/if}
</section>


<style>
    .display-songs h2 {
    color: #f2d9ff;
    font-size: 1.4rem;
    margin-bottom: 1.25rem;
    text-shadow: 0 0 10px rgba(199, 125, 255, 0.6);
}


.songs-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
}

.song-card {
    background: linear-gradient(160deg, #0b0014, #16001f);
    border: 1px solid rgba(199, 125, 255, 0.3);
    border-radius: 16px;
    padding: 1.1rem;
    position: relative;
    cursor: pointer;

    box-shadow:
        inset 0 0 14px rgba(180, 120, 255, 0.12),
        0 0 20px rgba(120, 60, 255, 0.25);

    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.song-card:hover {
    transform: translateY(-3px);
    box-shadow:
        inset 0 0 18px rgba(199, 125, 255, 0.2),
        0 0 30px rgba(199, 125, 255, 0.55);
}

.song-card:focus {
    outline: 2px solid rgba(199, 125, 255, 0.6);
    outline-offset: 2px;
}

.card-overlay {
    position: absolute;
    bottom: 1rem;
    right: 1rem;
    background: linear-gradient(135deg, #c77dff, #7b2cbf);
    color: #fff;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 600;
    opacity: 0;
    transition: opacity 0.25s ease;
    box-shadow: 0 0 12px rgba(199, 125, 255, 0.5);
}

.song-card:hover .card-overlay {
    opacity: 1;
}


.song h3 {
    color: #ffffff;
    font-size: 1.05rem;
    margin-bottom: 0.6rem;
    text-shadow: 0 0 10px rgba(199, 125, 255, 0.8);
}

.song-details p {
    font-size: 0.8rem;
    color: #d6bfff;
    margin: 0.2rem 0;
}

.song-details span {
    color: #e6ccff;
    font-weight: 500;
}

.song-details .name {
    color: #c77dff;
}

.lyrics {
    margin-top: 0.75rem;
    font-size: 0.8rem;
    line-height: 1.5;
    color: #e6ccff;

    max-height: 8rem;
    overflow-y: auto;

    padding: 0.5rem 0.6rem 0.5rem 0.9rem;

    border-top: 1px solid rgba(199, 125, 255, 0.25);
    border-left: 2px solid rgba(199, 125, 255, 0.35);

    background: linear-gradient(
        90deg,
        rgba(199, 125, 255, 0.08),
        rgba(11, 0, 20, 0.0) 40%
    );

    box-shadow: inset 0 0 12px rgba(180, 120, 255, 0.12);
}

.lyrics::-webkit-scrollbar {
    width: 8px;
}

.lyrics::-webkit-scrollbar-track {
    background: rgba(20, 0, 40, 0.5);
    border-radius: 6px;
}

.lyrics::-webkit-scrollbar-thumb {
    background: linear-gradient(
        180deg,
        #c77dff,
        #7b2cbf
    );
    border-radius: 6px;
    box-shadow: 0 0 8px rgba(199, 125, 255, 0.6);
}

.lyrics::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(
        180deg,
        #e0aaff,
        #9d4edd
    );
}

/* Firefox */
.lyrics {
    scrollbar-width: thin;
    scrollbar-color: #c77dff rgba(20, 0, 40, 0.6);
}


.lyrics::after {
    content: "";
    position: sticky;
    bottom: 0;
    display: block;
    height: 12px;
    background: linear-gradient(
        to top,
        rgba(11, 0, 20, 0.8),
        transparent
    );
    pointer-events: none;
}


.display-songs > p {
    color: #caa6ff;
    font-style: italic;
    text-align: center;
    margin-top: 3rem;
}
/*  */
</style>
