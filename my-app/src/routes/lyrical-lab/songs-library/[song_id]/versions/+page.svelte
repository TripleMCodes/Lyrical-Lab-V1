
<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
     import { editingSong } from '$lib/stores/editingSong';
    import type {PageData} from './$types';

    let {data} = $props<{ data: PageData }>();
    const song = data.versions[0]; // Get the original version of the song
    const song_id = data.song.song_id;

    const goBack = () => {
        goto('/lyrical-lab/songs-library');
    };

    const delete_song = async () => {
        if (confirm('Are you sure you want to delete this song? This action cannot be undone.')) {
            try {
                const response = await fetch(`/api/songs/${song.id}`, {
                    method: 'DELETE'
                });
                if (response.ok) {
                    alert('Song deleted successfully.');
                    goto('/lyrical-lab/songs-library');
                } else {
                    alert('Failed to delete the song. Please try again.');
                }
            } catch (error) {
                console.error('Error deleting song:', error);
                alert('An error occurred while deleting the song. Please try again.');


            }        }
    };                          
 
    // const delete_song = () => {
    // if (confirm('Are you sure you want to delete this song? This action cannot be undone.')) {
    //     fetch(`/api/songs/${song.id}`, {                                              

    //             method: 'DELETE'
    //         })
    //         .then(response => {    
    //             if (response.ok) {
    //                 alert('Song deleted successfully.');                                                                                 
    //                 goto('/lyrical-lab/songs-library');
    //             } else {   
    //                 alert('Failed to delete the song. Please try again.');
    //             }  
    //         })
    //         .catch(error => {  
    //             console.error('Error deleting song:', error);
    //             alert('An error occurred while deleting the song. Please try again.');
    //         });
    //     }


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
        </div>
    </div>
</div>  