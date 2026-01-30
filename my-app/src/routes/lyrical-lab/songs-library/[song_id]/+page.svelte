<script lang="ts">
    import type { PageData } from './$types';
    import { goto } from '$app/navigation';
    import { editingSong } from '$lib/stores/editingSong';

    let { data } = $props<{ data: PageData }>();
    const song = data.song;

    const goBack = () => {
        goto('/lyrical-lab/songs-library');
    };

    const update_song = () => {
    editingSong.set(song);   
    goto('/lyrical-lab');
    };
</script>

<div class="song-detail-container">
    <button class="back-btn" onclick={goBack}>
        ← Back to Library
    </button>

    <div class="song-header">
        <h1>{song.song_name}</h1>
        <div class="header-meta">
            <div class="meta-item">
                <span class="label">Artist</span>
                <span class="value">{song.song_artist}</span>
            </div>
            <div class="meta-item">
                <span class="label">Genre</span>
                <span class="value">{song.song_genre}</span>
            </div>
            {#if song.song_mood}
                <div class="meta-item">
                    <span class="label">Mood</span>
                    <span class="value">{song.song_mood}</span>
                </div>
            {/if}
            {#if song.song_album}
                <div class="meta-item">
                    <span class="label">Album</span>
                    <span class="value">{song.song_album}</span>
                </div>
            {/if}
            <div class="meta-item">
                <span class="label">Created</span>
                <span class="value">{new Date(song.date_created).toLocaleDateString()}</span>
            </div>
            {#if song.date_modified !== song.date_created}
                <div class="meta-item">
                    <span class="label">Modified</span>
                    <span class="value">{new Date(song.date_modified).toLocaleDateString()}</span>
                </div>
            {/if}
        </div>
    </div>

    <div class="lyrics-container">
        <h2>Lyrics</h2>
        <div class="lyrics-text">
            {song.song_lyrics}
        </div>
        <div>
            <button onclick={update_song}>Update</button>
        </div>
    </div>
</div>

<style>
    .song-detail-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 2rem 1.5rem;
    }

    /* === BACK BUTTON === */
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
        margin-bottom: 2rem;

        box-shadow: 0 0 16px rgba(199, 125, 255, 0.45);
        transition: all 0.25s ease;
    }

    .back-btn:hover, button:hover {
        background: linear-gradient(135deg, #e0aaff, #9d4edd);
        box-shadow: 0 0 26px rgba(199, 125, 255, 0.7);
        transform: translateX(-2px);
    }

    .back-btn:active, button:active {
        transform: translateX(-1px);
    }

    /* === SONG HEADER === */
    .song-header {
        background: linear-gradient(160deg, #0b0014, #16001f);
        border: 1px solid rgba(199, 125, 255, 0.3);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;

        box-shadow:
            inset 0 0 14px rgba(180, 120, 255, 0.12),
            0 0 30px rgba(120, 60, 255, 0.25);
    }

    .song-header h1 {
        color: #ffffff;
        font-size: 2.2rem;
        margin: 0 0 1.5rem 0;
        text-shadow: 0 0 15px rgba(199, 125, 255, 0.8);
        line-height: 1.2;
    }

    /* === HEADER META === */
    .header-meta {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1.5rem;
    }

    .meta-item {
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
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

    /* === LYRICS CONTAINER === */
    .lyrics-container {
        background: linear-gradient(160deg, #0b0014, #16001f);
        border: 1px solid rgba(199, 125, 255, 0.3);
        border-radius: 16px;
        padding: 2rem;

        box-shadow:
            inset 0 0 14px rgba(180, 120, 255, 0.12),
            0 0 30px rgba(120, 60, 255, 0.25);
    }

    .lyrics-container h2 {
        color: #f2d9ff;
        font-size: 1.5rem;
        margin: 0 0 1.5rem 0;
        text-shadow: 0 0 10px rgba(199, 125, 255, 0.6);
    }

    .lyrics-text {
        color: #e6ccff;
        font-size: 1rem;
        line-height: 1.8;
        white-space: pre-wrap;
        word-wrap: break-word;

        padding: 1.5rem;
        background: linear-gradient(
            90deg,
            rgba(199, 125, 255, 0.08),
            rgba(11, 0, 20, 0.0) 40%
        );
        border-left: 3px solid rgba(199, 125, 255, 0.35);
        border-radius: 8px;

        box-shadow: inset 0 0 12px rgba(180, 120, 255, 0.12);
    }

    /* === RESPONSIVE === */
    @media (max-width: 768px) {
        .song-detail-container {
            padding: 1rem;
        }

        .song-header {
            padding: 1.5rem;
        }

        .song-header h1 {
            font-size: 1.6rem;
        }

        .header-meta {
            grid-template-columns: repeat(2, 1fr);
        }

        .lyrics-container {
            padding: 1.5rem;
        }

        .lyrics-text {
            padding: 1rem;
            font-size: 0.95rem;
        }
    }
</style>
