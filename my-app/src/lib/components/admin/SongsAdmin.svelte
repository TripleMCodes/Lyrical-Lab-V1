<script lang="ts">
    import { enhance } from '$app/forms';

    interface Song {
        song_id: number;
        song_name: string;
        song_artist: string;
        song_lyrics: string;
        user_name: string;
        date_created: string;
    }

    let { songs }: { songs: Song[] } = $props();

    let totalSongs = $derived(() => songs.length);
    let recentSongs = $derived.by(() => 
        songs
            .sort((a, b) => new Date(b.date_created).getTime() - new Date(a.date_created).getTime())
            .slice(0, 5)
    );

    // Group songs by user
    let songsByUser = $derived(() => {
        const grouped: { [key: string]: Song[] } = {};
        songs.forEach(song => {
            if (!grouped[song.user_name]) {
                grouped[song.user_name] = [];
            }
            grouped[song.user_name].push(song);
        });
        return grouped;
    });
</script>

<div class="songs-admin">
    <h2>Songs Management</h2>
    
    <div class="stats">
        <div class="stat">
            <h3>Total Songs</h3>
            <p>{totalSongs}</p>
        </div>
    </div>

    <div class="recent-songs">
        <h3>Recently Added Songs</h3>
        <ul>
            {#each recentSongs as song}
                <li>
                    <strong>{song.song_name}</strong> by {song.song_artist} - {song.user_name} ({new Date(song.date_created).toLocaleDateString()})
                </li>
            {/each}
        </ul>
    </div>

    <div class="songs-by-user">
        <h3>Songs by User</h3>
        {#each Object.entries(songsByUser) as [user, userSongs]}
            <div class="user-section">
                <h4>{user} ({userSongs.length} songs)</h4>
                <ul>
                    {#each userSongs as song}
                        <li class="song-item">
                            <div class="song-info">
                                <strong>{song.song_name}</strong> by {song.song_artist} - {new Date(song.date_created).toLocaleDateString()}
                            </div>
                            <form method="POST" action="?/admin_delete_song" use:enhance>
                                <input type="hidden" name="song_id" value={song.song_id} />
                                <button type="submit" class="delete-btn">Delete</button>
                            </form>
                        </li>
                    {/each}
                </ul>
            </div>
        {/each}
    </div>
</div>

<style>
    .songs-admin {
        margin-top: 2rem;
        padding: 1rem;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        background: #f9fafb;
    }

    .songs-admin h2 {
        margin-bottom: 1rem;
        color: #111827;
    }

    .stats {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .stat {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    .stat h3 {
        margin: 0;
        font-size: 0.875rem;
        color: #6b7280;
    }

    .stat p {
        margin: 0.5rem 0 0;
        font-size: 1.5rem;
        font-weight: bold;
        color: #111827;
    }

    .recent-songs, .songs-by-user {
        margin-bottom: 1.5rem;
    }

    .recent-songs h3, .songs-by-user h3 {
        margin-bottom: 0.5rem;
        color: #374151;
    }

    .recent-songs ul, .songs-by-user ul {
        list-style: none;
        padding: 0;
    }

    .recent-songs li, .song-item {
        padding: 0.5rem;
        background: white;
        border-radius: 0.25rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }

    .user-section h4 {
        margin: 1rem 0 0.5rem;
        color: #4b5563;
    }

    .song-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .song-info {
        flex: 1;
    }

    .delete-btn {
        background: #dc2626;
        color: white;
        border: none;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        cursor: pointer;
        font-size: 0.875rem;
    }

    .delete-btn:hover {
        background: #b91c1c;
    }
</style>