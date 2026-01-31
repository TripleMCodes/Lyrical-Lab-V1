<script lang="ts">
  import type { PageData } from './$types';
  import { goto } from '$app/navigation';
  import DisplaySongs from "../../../lib/components/DisplaySongs.svelte";
  import SongsFilter from '$lib/components/SongsFilter.svelte';

  let { data } = $props<{ data: PageData }>();

  // these will change when the route reloads
  let allSongs = $derived(data.songs);
  let meta = $derived(data.meta);

  // keep in sync when navigation changes data
  $effect(() => {
    allSongs = data.songs;
    meta = data.meta;
  });

  let filteredSongs = $derived([...allSongs]);

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

      if (filters.genre && song.song_genre !== filters.genre) matches = false;
      if (filters.mood && song.song_mood !== filters.mood) matches = false;
      if (filters.album && song.song_album !== filters.album) matches = false;

      if (filters.dateFrom) {
        const songDate = new Date(song.date_created);
        const fromDate = new Date(filters.dateFrom);
        if (songDate < fromDate) matches = false;
      }

      if (filters.dateTo) {
        const songDate = new Date(song.date_created);
        const toDate = new Date(filters.dateTo);
        if (songDate > toDate) matches = false;
      }

      return matches;
    });
  });

  const resetFilters = () => {
    filters = { genre: '', mood: '', album: '', dateFrom: '', dateTo: '' };
  };

  const handleSongClick = (songId: number) => {
    goto(`/lyrical-lab/songs-library/${songId}`);
  };

  const nextPage = () => {
    if (!meta.next_page) return;
    goto(`/lyrical-lab/songs-library?page=${meta.next_page}&size=${meta.size}`);
  };

  const prevPage = () => {
    if (!meta.prev_page) return;
    goto(`/lyrical-lab/songs-library?page=${meta.prev_page}&size=${meta.size}`);
  };

    let genres = $derived([...new Set(allSongs.map(s => s.song_genre))]);
    let moods = $derived([...new Set(allSongs.map(s => s.song_mood).filter(Boolean))]);
    let albums = $derived([...new Set(allSongs.map(s => s.song_album).filter(Boolean))]);

  $effect(() =>{
    genres = [...new Set(allSongs.map(s => s.song_genre))];
    moods = [...new Set(allSongs.map(s => s.song_mood).filter(Boolean))];
    albums = [...new Set(allSongs.map(s => s.song_album).filter(Boolean))];
  }
  )

</script>

<SongsFilter bind:filters={filters} genres={genres} moods={moods} albums={albums} resetFilters={resetFilters} />

<DisplaySongs bind:filteredSongs={filteredSongs} handleSongClick={handleSongClick} />

<div>
  <button onclick={prevPage} disabled={!meta.prev_page}>prev</button>
  <span>page {meta.page} / {meta.pages}</span>
  <button onclick={nextPage} disabled={!meta.next_page}>next</button>
</div>
