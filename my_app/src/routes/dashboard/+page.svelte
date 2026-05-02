<script lang="ts">
    import Stats from "$lib/components/Stats.svelte";
    import Workspace from "$lib/components/Workspace.svelte";
    import RimeSearch from "$lib/components/RimeSearch.svelte";
    import Scratchpad from "$lib/components/Scratchpad.svelte";
    import Search from "$lib/components/Search.svelte";
    import Notification from "$lib/components/Notification.svelte";
    import Chart from "$lib/components/Chart.svelte"
    import {debounce} from "$lib/api/debounce"
    import type { PageData } from "../$types";
    import { goto } from '$app/navigation'
    import { editingSong } from "$lib/stores/editingSong";
    import {fetchRhymes} from '$lib/api/lyric_tools'
    import {get_url} from '$lib/url_vars/urls_vars'
//   import SigilSpinner from '$lib/components/SigilSpinner.svelte';


    let { data } = $props<{ data: PageData }>();

    // svelte-ignore state_referenced_locally
    let writing_time = $state(data.stats.writing_time)

    console.log("WRITING TIME:", writing_time)

    let minutes = $derived(Math.floor(writing_time / 60))
    let seconds = $derived(writing_time % 60)
    let hours = $derived(Math.floor(minutes / 60))

    let formatted_time = $derived(`${hours}h ${minutes % 60}m ${seconds}s`)

    // svelte-ignore state_referenced_locally
    let writing_sessions = $state(data.stats.writing_sessions)
    // svelte-ignore state_referenced_locally
    let new_songs = $state(data.songs_stats.new_songs)
    // svelte-ignore state_referenced_locally
    let num_songs = $state(data.songs_stats.num_songs)

    // svelte-ignore state_referenced_locally    
    let draft_artist = $state(data.draft.song_artist)
    // svelte-ignore state_referenced_locally
    let draft_title = $state(data.draft.song_name)
    // svelte-ignore state_referenced_locally
    let draft_album = $state(data.draft.song_album)
    // svelte-ignore state_referenced_locally
    let recentSongs = $state(data.recent_songs)
    // svelte-ignore state_referenced_locally
    let notes = $state(data.notes)
    let note = $state("")
    let currentNoteId = $state("")

    let rhyme = $state("")
    let wordList = $state([])
    let phraseList = $state([])
    let isLoading = $state(false)

    let searchDisplay = $state(false)
    let searchResults = $state([])


    let showNotification = $state(false);
    let notificationMessage = $state("");
    let notificationType = $state("success");



    function openStudio (){
       editingSong.set(data.draft)
       goto('/lyrical-lab')
    }

    async function openSongFromSearch(song) {
        // Fetch the full song data from the backend using the doc_id
        try {
            const songId = parseInt(song.doc_id);
            const res = await fetch(`${get_url()}/api/lyric-tools/user-songs/${songId}`, {
                method: "GET",
                credentials: "include"
            });

            if (res.ok) {
                const songData = await res.json();
                editingSong.set(songData);
                goto('/lyrical-lab');
            } else {
                notificationMessage = "Failed to load song";
                notificationType = "error";
                showNotification = true;
            }
        } catch (error) {
            notificationMessage = "Error loading song";
            notificationType = "error";
            showNotification = true;
        }
    }

    function viewNote(note_content, note_id){
        note = note_content;
        currentNoteId = note_id
    }

    async function updateSongsList() {
        const res5 = await fetch(`${get_url()}/api/lyric-tools/get-notes`, {
        method: "GET",
        credentials: "include"
    });

        if (res5.ok) {
            notes = await res5.json()
        }
    }

    async function saveNote(){

        if (!note){
             notificationMessage = "Error - note to save empty";
            notificationType = "error";
            showNotification = true;
            return
        }

        try{
            const res = await fetch(
                `${get_url()}/api/lyric-tools/save-note`,
                {
                    method: 'POST', 
                    credentials: 'include',
                    headers:{
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({"note": note, "id":currentNoteId})
                }
            )
            const res_data = await res.json();
            updateSongsList()
            notificationMessage = res_data.message;
            notificationType = "success";
            showNotification = true;

        }catch(err){
            notificationMessage = "Couldn't process lines";
            notificationType = "error";
            showNotification = true;
        }


    }

    async function delNote(id){
        console.log(id)
        // id = Number(id)
        try{
            const res = await fetch(`${get_url()}/api/lyric-tools/notes/${id}`,
                {
                    method: 'DELETE',
                    credentials: 'include'
                }
            )

            const res_data = await res.json();
            updateSongsList()
            notificationMessage = res_data.message;
            notificationType = "success";
            showNotification = true;
        }catch(error){
            notificationMessage = "Couldn't process lines";
            notificationType = "error";
            showNotification = true;
        }

    }

    function createNote(){
        currentNoteId = ""
        note = ""
    }

    async function findRhyme(){
        console.log("rime button click!")
        
        isLoading = true;
        const lst = await fetchRhymes(rhyme);
        console.log("the rhyme list is", lst);
       
        wordList = lst.word_rhymes;
        phraseList = lst.phrasal_rhymes;
        isLoading = false;
    }
    $inspect(recentSongs);

    const dfindRhyme = debounce(findRhyme, 100);
    const dopenSongFromSearch = debounce(openSongFromSearch, 100)
</script>

<section class="container">
    <div class="main scrollable">
        <!-- search coming soon -->
        <!-- <Search bind:display={searchDisplay} bind:results={searchResults} openSong={dopenSongFromSearch}/> -->

        <Scratchpad viewNote={viewNote} makeNewNote={createNote} delNote={delNote} saveNote={saveNote} bind:notes={notes} bind:note={note} />

        <RimeSearch findRhyme={dfindRhyme} bind:rhyme={rhyme} bind:rime_list={wordList} bind:phraseList={phraseList} bind:isLoading={isLoading} />
    </div>

    <div class="main scrollable">
        
        <Stats bind:writing_time={formatted_time} bind:writing_sessions={writing_sessions} bind:new_songs={new_songs} bind:num_songs={num_songs}/>
        <Chart></Chart>
        <Workspace openStudio={openStudio} bind:artist={draft_artist} bind:title={draft_title} bind:album={draft_album} bind:recent_songs={recentSongs}/>


    </div>
</section>

<Notification 
    bind:show={showNotification}
    bind:message={notificationMessage}
    bind:type={notificationType}
    on:close={() => showNotification = false}
/>

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
    margin-left:1rem;
    margin-right:1rem;
    flex: 1;
    display: flex;
    width: 130%;
    padding: 1rem;
    box-sizing: border-box;
    align-items: stretch;
}

/* ===== Main panels ===== */
.main {
    flex: 1;                 
    min-height: 0;          
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
    overflow-y:scroll;
}

/* .main > * {
    flex-shrink: 0;
} */

/* If one section should scroll */
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

/* =========================================
   MEDIA QUERIES — Dashboard / Home Layout
   xs: < 375px  |  sm: 375–639px  |  md: 640–1023px
   lg: 1024–1279px  |  xl: 1280+  |  2xl: 1600+
   ========================================= */

/* -----------------------------------------
   XS — Very small phones (< 375px)
   ----------------------------------------- */
@media (max-width: 374px) {
  .container {
    flex-direction: column-reverse;   /* Two panels stack vertically */
    width: 100%;
    margin-left: 0;
    margin-right: 0;
    padding: 0.5rem;
    gap: 0.5rem;
  }

  .main {
    flex: 0 0 auto;           /* Let content define height when stacked */
    min-height: 60dvh;        /* Enough room to be useful */
    padding: 1rem;
    border-radius: 14px;
    gap: 0.75rem;
    backdrop-filter: blur(8px);   /* Reduce blur cost on low-end phones */
    -webkit-backdrop-filter: blur(8px);
  }

  .main::-webkit-scrollbar {
    width: 5px;
  }
}

/* -----------------------------------------
   SM — Standard phones (375px – 639px)
   ----------------------------------------- */
@media (min-width: 375px) and (max-width: 639px) {
  .container {
    flex-direction: column-reverse;
    width: 100%;
    margin-left: 0;
    margin-right: 0;
    padding: 0.75rem;
    gap: 0.75rem;
  }

  .main {
    flex: 0 0 auto;
    min-height: 65dvh;        /* Each panel gets enough vertical room */
    padding: 1.1rem;
    border-radius: 16px;
    gap: 0.875rem;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
  }

  .main::-webkit-scrollbar {
    width: 6px;
  }
}

/* -----------------------------------------
   MD — Large phones / small tablets (640px – 1023px)
   ----------------------------------------- */
@media (min-width: 640px) and (max-width: 1023px) {
  .container {
    flex-direction: column-reverse;   /* Still stacked — not enough width for two panels */
    width: 100%;
    margin-left: 0.5rem;
    margin-right: 0.5rem;
    padding: 0.875rem;
    gap: 0.875rem;
  }

  .main {
    flex: 0 0 auto;
    min-height: 55dvh;        /* Shorter — two panels visible on screen together */
    padding: 1.25rem;
    border-radius: 18px;
    gap: 1rem;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
  }

  .main::-webkit-scrollbar {
    width: 7px;
  }
}

/* -----------------------------------------
   LG — Tablets / small laptops (1024px – 1279px)
   ----------------------------------------- */
@media (min-width: 1024px) and (max-width: 1279px) {
  .container {
    flex-direction: row;      /* Side-by-side panels return at tablet landscape */
    width: 110%;              /* Step down from 130% */
    margin-left: 0.75rem;
    margin-right: 0.75rem;
    padding: 0.875rem;
    gap: 0.875rem;
    align-items: stretch;
  }

  .main {
    flex: 1;
    min-height: 0;
    padding: 1.25rem;
    border-radius: 20px;
    gap: 0.875rem;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
  }

  .main::-webkit-scrollbar {
    width: 8px;
  }
}

/* -----------------------------------------
   XL — Standard desktops (1280px – 1599px)
   ----------------------------------------- */
@media (min-width: 1280px) {
  /* Base styles are tuned for this range — preserved.
     width: 130%, flex-direction: row, padding: 1rem,
     margin: 1rem are all intentional. */

  .container {
    gap: 1rem;                /* Explicit gap between the two .main panels */
  }

  .main {
    padding: 1.5rem;          /* Matches base */
    border-radius: 22px;
    gap: 1rem;
  }

  .main::-webkit-scrollbar {
    width: 10px;              /* Matches base */
  }
}

/* -----------------------------------------
   2XL — Large / wide monitors (1600px+)
   ----------------------------------------- */
@media (min-width: 1600px) {
  .container {
    width: 120%;              /* Expand slightly on large monitors */
    padding: 1.25rem;
    margin-left: 1.25rem;
    margin-right: 1.25rem;
    gap: 1.25rem;
  }

  .main {
    padding: 2rem;
    border-radius: 26px;
    gap: 1.25rem;
    box-shadow:
      0 0 40px rgba(168, 85, 247, 0.22),
      inset 0 0 0 1px rgba(255, 255, 255, 0.05);
  }

  .main::-webkit-scrollbar {
    width: 12px;
  }
}

</style>
