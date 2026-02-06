<script lang="ts">
    import Stats from "$lib/components/Stats.svelte";
    import Workspace from "$lib/components/Workspace.svelte";
    import RimeSearch from "$lib/components/RimeSearch.svelte";
    import Scratchpad from "$lib/components/Scratchpad.svelte";
    import Search from "$lib/components/Search.svelte";
    import type { PageData } from "../$types";
    import { goto } from '$app/navigation'
    import { editingSong } from "$lib/stores/editingSong";

    let { data } = $props<{ data: PageData }>();

    let writing_time = $state(data.stats.writing_sessions)
    let writing_sessions = $state(data.stats.total_writing_time)
    let new_songs = $state(data.songs_stats.new_songs)
    let num_songs = $state(data.songs_stats.num_songs)

    let draft_artist = $state(data.draft.song_artist)
    let draft_title = $state(data.draft.song_name)
    let draft_album = $state(data.draft.song_album)

    let recentSongs = $state(data.recent_songs);

    function openStudio (){
       editingSong.set(data.draft)
       goto('/lyrical-lab')
    }


    $inspect(recentSongs)


</script>


<section class="container">
    <div class="main scrollable">
        <Search/>
        <Scratchpad/>
        <RimeSearch/>
    </div>

    <div class="main scrollable">
        
        <Stats bind:writing_time={writing_time} bind:writing_sessions={writing_sessions} bind:new_songs={new_songs} bind:num_songs={num_songs}/>

        <Workspace openStudio={openStudio} bind:artist={draft_artist} bind:title={draft_title} bind:album={draft_album} bind:recent_songs={recentSongs}/>


    </div>
</section>

<style>
:root {
    --purple-900: #120018;
    --purple-800: #1a0024;
    --purple-600: #7c3aed;
    --purple-500: #a855f7;

    --glass-bg: rgba(40, 10, 60, 0.45);
    --glass-border: rgba(168, 85, 247, 0.25);
    --glass-highlight: rgba(168, 85, 247, 0.45);
}

/* ===== Container ===== */
.container {
    /* display: flex;
    gap: 1rem;
    padding: 1rem;

    width: 100%;
    height: 100vh;

    /* THIS is the fix */
    margin-left:1rem;
    margin-right:1rem;
    /* gap: 1rem; */
    flex: 1;
    display: flex;

    width: 130%;
    /* height: 200%; */

    padding: 1rem;
    box-sizing: border-box;
    align-items: stretch;
}

/* ===== Main panels ===== */
.main {
    flex: 1;                 /* equal width */
    height: 100%;            /* equal height */
    min-height: 0;           /* allows inner scrolling */

    display: flex;
    flex-direction: column;
    gap: 1rem;

    background: linear-gradient(
        180deg,
        rgba(120, 50, 180, 0.25),
        rgba(25, 8, 40, 0.55)
    );

    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);

    border-radius: 22px;
    border: 1px solid var(--glass-border);

    box-shadow:
        0 0 30px rgba(168, 85, 247, 0.18),
        inset 0 0 0 1px rgba(255, 255, 255, 0.04);

    padding: 1.5rem;

    color: #f5e9ff;

    /* Internal scroll instead of breaking height */
    overflow: hidden;
}

/* Optional: allow content scrolling */
.main > * {
    flex-shrink: 0;
}

/* If one section should scroll (recommended) */
.main.scrollable {
    overflow-y: auto;
}

.main::-webkit-scrollbar {
        width: 10px;
        }

.main::-webkit-scrollbar-track{
    background: rgba(20, 0, 40, 0.6);
    border-radius: 8px;
}

.main::-webkit-scrollbar-thumb {
        background: linear-gradient(
            180deg,
            #c77dff,
            #7b2cbf
        );
        border-radius: 8px;
        box-shadow: 0 0 8px rgba(199, 125, 255, 0.6);
        } 


.main::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(
            180deg,
            #e0aaff,
            #9d4edd
        );
        }

.main {
        scrollbar-width: thin;
        scrollbar-color: #c77dff rgba(20, 0, 40, 0.6);
        }  


</style>
