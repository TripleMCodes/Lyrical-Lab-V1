<script>
    // @ts-ignore
    import { text } from "@sveltejs/kit";
    // @ts-ignore
    import Editor from '../../lib/components/SplitEditor.svelte'
    import Controls from '../../lib/components/Controls.svelte'
    import SongPanel from '../../lib/components/SongPanel.svelte'
    import Notification from '../../lib/components/Notification.svelte'
  import { FileWatcherEventKind } from "typescript";
  // import { words } from "../sverdle/words.server";
  let words = $state(0);
  let chars = $state(0);
  let editorContent = $state("");
  let title = $state("");
  let artist = $state("");
  let album = $state("");
  let mood = $state("");
  let genre = $state("");

  let showNotification = $state(false);
  let notificationMessage = $state("");
  let notificationType = $state("success");

  function notify(n){
    notificationMessage = `Please provide ${n}`;
    notificationType = "error";
    showNotification = true;
  }

  async function handleSave() {
    console.log("button pressed");

    let data = {};
    if (!title || !artist || !editorContent){
      if (!title) notify("Title")
      if (!artist) notify("Artist")
      if (!editorContent) notify("Lyrics")
      return
    }

    data["song_name"] = title;
    data["song_artist"] = artist;
    data["song_lyrics"] = editorContent;
    if (mood) data["song_mood"] = mood;
    if (genre) data["song_genre"] = genre;
    if (album) data["song_album"] = album;

    try {
        const res = await fetch(
            "http://localhost:8000/api/lyric-tools/save-song",
            {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            }
        );
        const msg = await res.json();
        console.log(msg);

        if (res.ok) {
            notificationMessage = msg.message || "Song saved successfully!";
            notificationType = "success";
            showNotification = true;
        } else {
            notificationMessage = msg.message || "Failed to save song";
            notificationType = "error";
            showNotification = true;
        }
    } catch (err) {
        console.log(err);
        notificationMessage = "Network error: Failed to save song";
        notificationType = "error";
        showNotification = true;
    }
}
    // let collapsed = $state(false);
    // import icon1 from '../../../public/icons8-brain-64.png'
</script>


<SongPanel bind:title bind:artist bind:album bind:mood bind:genre />
<section  class="ll-container" >
  <Controls onSave={handleSave} />
  <Editor bind:editor1={editorContent} bind:wordCount={words} bind:charCount={chars} />
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

    width: 150%;
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

/* Optional emphasis when typing */
.word-counter.active span {
  animation: pulseGlow 1.2s ease-in-out infinite;
}

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



</style> 