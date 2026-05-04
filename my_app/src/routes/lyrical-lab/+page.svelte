<script lang="ts">
    // @ts-ignore
    import Editor from '../../lib/components/SplitEditor.svelte'
    import Controls from '../../lib/components/Controls.svelte'
    import SongPanel from '../../lib/components/SongPanel.svelte'  
    import Notification from '../../lib/components/Notification.svelte'
    import WritingTimer from "../../lib/components/WritingTimer.svelte";
    import {fetchWords} from '../../lib/api/client'
    import {debounce} from "$lib/api/debounce"
    import {fetchRhymes} from '$lib/api/lyric_tools'
    import { get } from 'svelte/store';
    import type { PageData } from "../$types";
    import { editingSong } from '$lib/stores/editingSong';
    import {get_url} from '$lib/url_vars/urls_vars';
    import {apiPost} from '$lib/api/api_proxy'
    import {apiGet} from '$lib/api/api_proxy'

  let saved_song_id: Number = $state();
  let song_data;
  let { data } = $props<{ data: PageData }>();
  let song = $state(null);

  editingSong.subscribe(value => {
    if (value) {
        song = value;
        console.log('current editing song:', song);
    }
  });
  $effect(() => {
    console.log('the value of song is', song);
});

  // Fetch remaining requests on component mount
  async function fetchRequestsRemaining() {
    try {
      // const res = await fetch(
      //   `${get_url()}/api/lyric-tools/api-requests-remaining`,
      //   {
      //     method: "GET",
      //     credentials: "include",
      //     headers: {
      //       "Content-Type": "application/json"
      //     }
      //   }
      // );
      // const res = await apiGet(`/api/lyric-tools/api-requests-remaining`);
    
      const data = await apiGet(`/api/lyric-tools/api-requests-remaining`);
      requestsRemaining = data.requests_remaining;
      maxRequests = data.max_requests_per_day;
      
    } catch (err) {
      console.log("Error fetching requests remaining:", err);
    }
  }

  // Call on mount
  fetchRequestsRemaining();


  let words = $state(0);
  let chars = $state(0);
  let editorContent = $state("");
  let editor2Content = $state("");
  let title = $state("");
  let artist = $state("");
  let album = $state("");
  let mood = $state("");
  let genre = $state("");

  let wordSelected = $state("")
  let wordSearched = $state("")
  let wordList = $state<Array<{ word: string }>>([])
  let debounceTimer;

  let selectedValue = $state("")
  let selectedGenre = $state("Pop")
  let selectedFos = $state("Simile")
  let genInput = $state("")

  let isLoading = $state(false)

  let selectedText = $state("")
  
  let requestsRemaining = $state(5)
  let maxRequests = $state(5)

  let showNotification = $state(false);
  let notificationMessage = $state("");
  let notificationType = $state("success");

  function notify(n: string){
    notificationMessage = `Please provide ${n}`;
    notificationType = "error";
    showNotification = true;
  }


  async function handleSave() {

    
    let song_to_save = {};
    if (typeof saved_song_id === "number" && saved_song_id >= 0) {
      console.log("song id value", saved_song_id)
      song_to_save["song_id"] = saved_song_id;
      if (!title){
        notify("Please provide song title")
        return
      }
      song_to_save["song_name"] = title;
      if (!artist){
        notify("Please provide the artist's name")
        return
      }
      song_to_save["song_artist"] = artist;
      if (!editorContent){
        notify("Please provide lyrics")
        return
      }
      song_to_save["song_lyrics"] = editorContent;
      if (mood) song_to_save["song_mood"] = mood;
      if (genre) song_to_save["song_genre"] = genre;
      if (album) song_to_save["song_album"] = album;
      
    }
    else{
      if (!title || !artist || !editorContent){
        if (!title) notify("Title")
        if (!artist) notify("Artist")
        if (!editorContent) notify("Lyrics")
        return
      }

      song_to_save["song_name"] = title;
      song_to_save["song_artist"] = artist;
      song_to_save["song_lyrics"] = editorContent;
      if (mood) song_to_save["song_mood"] = mood;
      if (genre) song_to_save["song_genre"] = genre;
      if (album) song_to_save["song_album"] = album;

      // if updating existing song from songs library
      const s = get(editingSong);
      if (s && s.song_id){
        song_to_save['song_id'] = s.song_id;
      }else{
        song_to_save['song_id'] = null
      }

    }

    try {
        // const res = await fetch(
        //     `/lyrical-lab/save-song`,
        //     {
        //         method: "POST",
        //         credentials: "include",
        //         headers: {
        //             "Content-Type": "application/json"
        //         },
        //         body: JSON.stringify(song_to_save)
        //     }
        // );

        // const res = await apiPost(`/api/lyric-tools/save-song`, song_to_save)
        // const msg = await res.json();
        const msg = await apiPost(`/api/lyric-tools/save-song`, song_to_save)
        console.log(msg);

        if (msg.message === "Song saved successfully") {
            notificationMessage = msg.message || "Song saved successfully!";
            notificationType = "success";
            showNotification = true;
            song_data = msg.song;
            saved_song_id = song_data.song_id;
        } else {
            notificationMessage = msg.message || "Failed to save song";
            notificationType = "error";
            showNotification = true;
        }
    } catch (err) {
        if (err.message === "No changes"){
          notificationMessage = err.message;
        }
        else{
          notificationMessage = "Network error: Failed to save song";
        }
        notificationType = "error";
        showNotification = true;
    }

    increment_session_count();
}

  async function increment_session_count(){
    try{
      // const res = await fetch(`lyrical-lab/increment-session-count`, {
      //   method: "POST",
      //   headers: {
      //     "Content-Type": "application/json"
      //    },
      //     body: JSON.stringify({'sess': 1})
      // })


      const res = await apiPost(`/api/lyric-tools/increment-session`, {'sess': 1});

      // if (res.ok){
      //   console.log("session count incremented")
      // }
    }catch(err){
      console.log("Couldn't increment session count")
    }
  }

  async function fetchWordsWrapper(){
    isLoading = true
    console.log("Fetch ", wordSelected)
    if (wordSelected === "rhyme"){
      console.log("the rhyme is ", wordSearched)
      const data = await fetchRhymes(wordSearched)
      console.log('Rhyme data:', data)
      
      // Handle new rhyme response format with word_rhymes and phrasal_rhymes
      let combinedList = []
      
      if (data.phrasal_rhymes) {
        combinedList.push(...data.phrasal_rhymes.map(item => ({
          word: item.phrase,
          score: item.score,
          type: 'phrasal'
        })))
      }
      if (data.word_rhymes) {
        combinedList.push(...data.word_rhymes.map(item => ({
          word: item.word,
          score: item.score,
          type: 'word',
          input_word: item.input_word
        })))
      }
      
      
      wordList = combinedList
      
      if (wordList.length === 0){
        notificationMessage = "No rhymes found";
        notificationType = "error";
        showNotification = true;
        isLoading = false
      }
    }else{
      const lst = await fetchWords(wordSelected, wordSearched)
      wordList = lst
      console.log($state.snapshot(wordList))
      if (wordList.length === 0){
        notificationMessage = "No results found";
        notificationType = "error";
        showNotification = true;
        isLoading = false
      }
    }

    let textList = ""
    isLoading = false
    for (let index = 0; index < wordList.length; index++) {
      const item = wordList[index]
      // const score = item.score ? ` (${item.score.toFixed(2)})` : ''
      // const typeLabel = item.type && item.type === 'phrasal' ? ' [phrasal]' : ''
      // textList += item['word'] + score + typeLabel + '\n'
      textList += item['word'] + '\n'
    }
    editor2Content = textList
  }


  function createNewSong(){
    editingSong.set(null);
    editorContent = "";
    editor2Content = "";
    saved_song_id = null;
    title = "";
    artist = "";
    album = "";
    mood = "";
    genre = "";
  }

  function handleTextSelection(e) {
        const textarea = e.target;
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        selectedText = textarea.value.substring(start, end);
    }

    async function handleTextSelectionWrapper(){
      let lines = selectedText.split(/\r?\n/);

      if (!lines){
        notificationMessage = "Please select text, try again";
        notificationType = "error";
        showNotification = true;
        return
      }

      if (lines.length === 1 && lines[0] === ""){
        notificationMessage = "Please select text, try again";
        notificationType = "error";
        showNotification = true;
        return
        }
      
      try{
      //   const res = await fetch(
      //   `${get_url()}/api/lyric-tools/check-flow`,
      //   {
      //     method: 'POST',
      //     credentials: 'include',
      //     headers:{
      //       "Content-Type": "application/json"
      //     },
      //     body: JSON.stringify({'message': lines})
      //   }
      // );
      // const res = await apiPost(`/api/lyric-tools/check-flow`, {'message': lines});
      const data = await apiPost(`/api/lyric-tools/check-flow`, {'message': lines});
      editor2Content = data.message
      } catch (err){
        notificationMessage = "Couldn't process lines";
        notificationType = "error";
        showNotification = true;
      }
    }

    function cancleAction(){
      isLoading = false;
    }

    let draftData = {};
    
    function autoSave(){
      clearTimeout(debounceTimer)

      if (title) draftData["song_name"] = title
      if (artist) draftData["song_artist"] = artist
      if (editorContent) draftData["song_lyrics"] = editorContent
      if (album) draftData["song_album"] = album
      if (mood) draftData["song_mood"] = mood
      if (genre) draftData["song_genre"] = genre

      debounceTimer = setTimeout( async () => {
        try{
          // const res = await fetch(
          //   `lyrical-lab/save-draft`,
          //   {
          //     method: "POST",
          //     credentials: "include",
          //     headers:{
          //       "Content-Type": "application/json"
          //     },
          //     body: JSON.stringify(draftData)
          //   }
          // );
          const resData = await apiPost(`/api/lyric-tools/save-draft`, draftData);

          console.log("draft saved");
        }catch (err){
          notificationMessage = "Draft not saved - Pleased login again";
          notificationType = "error";
          showNotification = true;
          console.log("draft not saved - ", err);
          return
        }
      }, 3000)
    }

  function radioBtnChanged (event){
    selectedValue = event.target.value
  }

  async function generate(){
    console.log(selectedValue)
    console.log(selectedGenre)
    console.log(selectedFos)

    // Check if user has requests remaining
    if (requestsRemaining <= 0) {
      notificationMessage = "You have reached your daily limit of 5 requests. Please try again tomorrow.";
      notificationType = "error";
      showNotification = true;
      return
    }

    let data = {}

    if (!genInput){
      notificationMessage = "Please provide Lyric or Figure of speech";
      notificationType = "error";
      showNotification = true;
      return
    }

    if (selectedValue === "gen-fos"){
      data['mode'] = "gen-fos"
      if (!selectedFos){
        notificationMessage = "Please select a figure of speech (i.e simile, idiom)";
        notificationType = "error";
        showNotification = true;
        return
      }
      data["fos"] = selectedGenre;
      data["content"] = genInput;
    }
    else if(selectedValue === "gen-lyrics"){
      data["mode"] = "gen-lyrics"
      if (!selectedGenre){
        notificationMessage = "Please select a genre(i.e hip-hop, pop e.t.c)";
        notificationType = "error";
        showNotification = true;
        return
      }
      data["genre"] = selectedGenre
      data["content"] = genInput;
    }
    else{
      notificationMessage = "Please select option. lyrics gen mode or Figure of speech mode";
      notificationType = "error";
      showNotification = true;
      return
    }
    isLoading = true
    try{
      // const res = await fetch(
      //   `${get_url()}/api/lyric-tools/generate`,
      //   {
      //     method: "POST",
      //     credentials: "include",
      //     headers: {
      //       "Content-Type": "application/json"
      //     },
      //     body: JSON.stringify(data)
      //   }
      // );

      // const res = await apiPost(`/api/lyric-tools/generate`, data);
      
      // if (!res.ok) {
      //   const errorData = await res.json().catch(() => ({}));
      //   isLoading = false
      //   notificationMessage = errorData.detail || "An error occurred";
      //   notificationType = "error";
      //   showNotification = true;
      //   return;
      // }
      
      const msg = await apiPost(`/api/lyric-tools/generate`, data);

      isLoading = false
      console.log(msg)
      editor2Content = msg
      
      // Update remaining requests
      requestsRemaining = Math.max(0, requestsRemaining - 1);
      
    } catch (err){
      isLoading = false
       notificationMessage = err.message;
        notificationType = "error";
        showNotification = true;
    }

  }

  function selectedGenreChanged (event){
    selectedGenre = event.target.value;
  }

  function selectedFosChanged(event){
    selectedFos = event.target.value;
  }


  // svelte-ignore state_referenced_locally
  if (song && song != null){
     const draft = song.draft_data;
    title = song.song_name ?? '';
    editorContent = song.song_lyrics ?? '';
    genre = song.song_genre ?? '';
    mood = song.song_mood ?? '';
    artist = song.song_artist ?? '';
    saved_song_id = song.song_id
  }

  else if (data && data.draft_data) {
    const draft = data.draft_data;
    title = draft.song_name ?? '';
    editorContent = draft.song_lyrics ?? '';
    // console.log(editorContent)
    genre = draft.song_genre ?? '';
    mood = draft.song_mood ?? '';
    artist = draft.song_artist ?? '';
  }

   
  const dhandleSave = debounce(handleSave, 100);
  const dgenerate = debounce(generate, 100);
  // const dfetchWordsWrapper = debounce(fetchWordsWrapper, 100);
  const dhandleTextSelectionWrapper = debounce(handleTextSelectionWrapper, 100);
</script>


<SongPanel bind:title bind:artist bind:album bind:mood bind:genre />

<WritingTimer idleSeconds={10} />
<section  class="ll-container" >

  <Controls onSave={dhandleSave} bind:selected={wordSelected} bind:word={wordSearched} searchWord={fetchWordsWrapper} checkFlow={dhandleTextSelectionWrapper} bind:selectedValue={selectedValue} handleChange={radioBtnChanged} generate={dgenerate} bind:selectedGenre={selectedGenre} handleGenreChange={selectedGenreChanged} bind:selectedFos={selectedFos} handleFosChange={selectedFosChanged} bind:genInput={genInput} createNewSong={createNewSong}/>

  
    <Editor bind:editor1={editorContent} bind:wordCount={words} bind:charCount={chars} bind:editor2={editor2Content} bind:selectedText={selectedText} onSelected={handleTextSelection} bind:loading={isLoading} cancelRes={cancleAction} saveDraft={autoSave}/>
  
</section>

<section class="word-counter">
  <div>
    <label for="words">Words: </label>
    <span>{words}</span>
  </div>

  <div>
    <label for="chars">Characters: </label>
    <span>{chars}</span>
  </div>

  <div>
    <label for="requests">AI Requests Left: </label>
    <span class={requestsRemaining === 0 ? 'no-requests' : ''}>{requestsRemaining}/{maxRequests}</span>
  </div>
</section>

<Notification
  bind:show={showNotification}
  bind:message={notificationMessage}
  bind:type={notificationType}
  on:close={() => showNotification = false}
/>


 <style>

  .ll-container {
    flex: 1;
    display: flex;

    width: 130%;
    height: 200%;

    padding: 1rem;
    box-sizing: border-box;
  }

  .word-counter {
  display: flex;
  gap: 24px;
  align-items: center;

  padding: 14px 20px;
  border-radius: 16px;

  background: linear-gradient(145deg, #0b0518, #140a26);
  border: 1px solid rgba(180, 120, 255, 0.18);

  box-shadow:
    inset 0 0 14px rgba(180, 120, 255, 0.12),
    0 10px 26px rgba(0, 0, 0, 0.55);

  color: #efe6ff;
  font-family: system-ui, -apple-system, sans-serif;
}

/* Each stat block */
.word-counter > div {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

/* Labels */
.word-counter label {
  font-size: 0.7rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #c9a7ff;
}

/* Numbers */
.word-counter span {
  font-size: 1.1rem;
  font-weight: 600;
  color: #f5ecff;

  text-shadow:
    0 0 6px rgba(199, 125, 255, 0.45),
    0 0 14px rgba(199, 125, 255, 0.25);
}

.word-counter span.no-requests {
  color: #ff6b6b;
  text-shadow:
    0 0 6px rgba(255, 107, 107, 0.45),
    0 0 14px rgba(255, 107, 107, 0.25);
}

/* Optional emphasis when typing */
/* .word-counter.active span {
  animation: pulseGlow 1.2s ease-in-out infinite;
} */

/* Glow animation */
@keyframes pulseGlow {
  0%, 100% {
    text-shadow:
      0 0 6px rgba(199, 125, 255, 0.4),
      0 0 14px rgba(199, 125, 255, 0.2);
  }
  50% {
    text-shadow:
      0 0 10px rgba(210, 160, 255, 0.65),
      0 0 22px rgba(210, 160, 255, 0.45);
  }
}

/* Compact mode */
@media (max-width: 500px) {
  .word-counter {
    gap: 16px;
    padding: 12px 16px;
  }

  .word-counter span {
    font-size: 1rem;
  }
}

/* =========================================
   MEDIA QUERIES — Main Page Layout
   xs: < 375px  |  sm: 375–639px  |  md: 640–1023px
   lg: 1024–1279px  |  xl: 1280+  |  2xl: 1600+
   ========================================= */

/* -----------------------------------------
   XS — Very small phones (< 375px)
   ----------------------------------------- */
@media (max-width: 374px) {
  .ll-container {
    flex-direction: column-reverse;   /* Controls stacks above Editor */
    width: 100%;
    height: auto;             /* Let content define height */
    min-height: 100dvh;
    padding: 0.5rem;
    gap: 0.5rem;
  }

  /* .editor-container{
    height: 100%;
  } */

  .word-counter {
    flex-direction: column;   /* Stack stat blocks vertically */
    align-items: flex-start;
    gap: 10px;
    padding: 12px 14px;
    border-radius: 12px;
    margin-top: 0.5rem;
  }

  .word-counter > div {
    width: 100%;
    justify-content: space-between; /* Label left, number right */
    gap: 0;
  }

  .word-counter label {
    font-size: 0.68rem;
  }

  .word-counter span {
    font-size: 1rem;
  }
}

/* -----------------------------------------
   SM — Standard phones (375px – 639px)
   ----------------------------------------- */
@media (min-width: 375px) and (max-width: 639px) {
  .ll-container {
    flex-direction: column-reverse;
    width: 100%;
    /* height: auto; */
    height: 400%;
    padding: 0.75rem;
    gap: 0.75rem;
    flex: none;
  }

  /* .editor-container{
    height: 500% !important;
  } */

  .word-counter {
    flex-wrap: wrap;          /* Stats wrap to a 2-col grid if needed */
    gap: 12px 20px;
    padding: 12px 16px;
    border-radius: 14px;
    margin-top: 0.75rem;
    height: 200%;
  }

  .word-counter > div {
    flex: 1 1 auto;
    min-width: 80px;
  }

  .word-counter label {
    font-size: 0.68rem;
  }

  .word-counter span {
    font-size: 1rem;          /* Already handled by your 500px rule */
  }
}

/* -----------------------------------------
   MD — Large phones / small tablets (640px – 1023px)
   ----------------------------------------- */
@media (min-width: 640px) and (max-width: 1023px) {
  .ll-container {
    flex-direction: column-reverse;   /* Still stacked — Controls as toolbar above Editor */
    width: 100%;
    height: auto;
    min-height: 100dvh;
    padding: 0.875rem;
    gap: 0.875rem;
  }

  .word-counter {
    flex-wrap: nowrap;        /* All three stats in one row from here up */
    gap: 18px;
    padding: 13px 18px;
    border-radius: 14px;
    margin-top: 0.875rem;
  }

  .word-counter > div {
    flex: 1 1 auto;
  }

  .word-counter label {
    font-size: 0.69rem;
  }

  .word-counter span {
    font-size: 1.05rem;
  }
}

/* -----------------------------------------
   LG — Tablets / small laptops (1024px – 1279px)
   ----------------------------------------- */
@media (min-width: 1024px) and (max-width: 1279px) {
  .ll-container {
    flex-direction: row;      /* Controls | Editor side-by-side returns here */
    width: 100%;              /* Step down from 130% */
    height: 175%;
    padding: 0.875rem;
    gap: 0;
  }

  .word-counter {
    gap: 20px;
    padding: 13px 18px;
    margin-top: 1rem;
  }

  .word-counter span {
    font-size: 1.05rem;
  }
}

/* -----------------------------------------
   XL — Standard desktops (1280px – 1599px)
   ----------------------------------------- */
@media (min-width: 1280px) {
  /* Base styles are intentional at this range.
     width: 130%, height: 200%, flex-direction: row
     are all preserved — no overrides needed. */

  .word-counter {
    gap: 24px;                /* Matches base */
    padding: 14px 20px;
    margin-top: 1rem;
  }
}

/* -----------------------------------------
   2XL — Large / wide monitors (1600px+)
   ----------------------------------------- */
@media (min-width: 1600px) {
  .ll-container {
    padding: 1.25rem;
  }

  .word-counter {
    gap: 32px;
    padding: 16px 24px;
    border-radius: 18px;
    margin-top: 1.25rem;
  }

  .word-counter > div {
    gap: 10px;
  }

  .word-counter label {
    font-size: 0.75rem;
    letter-spacing: 0.1em;
  }

  .word-counter span {
    font-size: 1.2rem;
  }
}
</style> 