<script lang="ts">
    import type { PageData } from './$types';
    import { goto } from '$app/navigation';
    import DisplaySongs from "../../../lib/components/DisplaySongs.svelte"
    import SongsFilter from '$lib/components/SongsFilter.svelte';

    let { data } = $props<{ data: PageData }>();
    
    let allSongs = data.songs;
    let filteredSongs = $state([...allSongs]);

    let filters = $state({
        genre: '',
        mood: '',
        album: '',
        dateFrom: '',
        dateTo: ''
    });

    $effect(() => {
        filteredSongs = allSongs.filter(song => {
            let matches = true;

            if (filters.genre && song.song_genre !== filters.genre) {
                matches = false;
            }

            if (filters.mood && song.song_mood !== filters.mood) {
                matches = false;
            }

            if (filters.album && song.song_album !== filters.album) {
                matches = false;
            }

            if (filters.dateFrom) {
                const songDate = new Date(song.date_created);
                const fromDate = new Date(filters.dateFrom);
                if (songDate < fromDate) {
                    matches = false;
                }
            }

            if (filters.dateTo) {
                const songDate = new Date(song.date_created);
                const toDate = new Date(filters.dateTo);
                if (songDate > toDate) {
                    matches = false;
                }
            }

            return matches;
        });
    });

    const resetFilters = () => {
        filters = {
            genre: '',
            mood: '',
            album: '',
            dateFrom: '',
            dateTo: ''
        };
    };

    const handleSongClick = (songId: number) => {
        goto(`/lyrical-lab/songs-library/${songId}`);
    };

    const genres = [...new Set(allSongs.map(s => s.song_genre))];
    const moods = [...new Set(allSongs.map(s => s.song_mood).filter(Boolean))];
    const albums = [...new Set(allSongs.map(s => s.song_album).filter(Boolean))];
</script>


<SongsFilter bind:filters={filters} genres={genres} moods={moods} albums={albums} resetFilters={resetFilters} />

<DisplaySongs bind:filteredSongs={filteredSongs} handleSongClick={handleSongClick} />


<style>
   
</style>