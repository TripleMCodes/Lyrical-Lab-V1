<script>
    let { title = $bindable(), artist = $bindable(), album = $bindable(), mood = $bindable(), genre = $bindable() } = $props();
</script>

<section  class="song-infor">
  <div class="song-name">
    <label for="title">Title: </label>
    <input type="text" name="title" id="title" bind:value={title}>
  </div>

  <div class="song-artist">
    <label for="artist">Artist: </label>
    <input type="text" name="artist" id="artist" bind:value={artist}>
  </div>

  <div class="song-album">
    <label for="album">Album: </label>
    <input type="text" name="album" id="album" placeholder="Optional" bind:value={album}>
  </div>

  <div class="song-mood">
    <label for="mood">Mood: </label>
    <input type="text" name="mood" id="mood" placeholder="Optional" bind:value={mood}>
  </div>

  <div class="song-genre">
    <label for="genre">Genre: </label>
    <input type="text" name="genre" id="genre" placeholder="Optional" bind:value={genre}>
  </div>
</section>

<style>
    section div{
        margin-left: 2rem;
        margin-right: 2rem;
    }

    .song-infor {
        display:flex;
        flex-direction: row;
        justify-content: space-evenly;

        padding: 20px 24px;
        border-radius: 18px;

        background: linear-gradient(145deg, #0b0518, #130a24);
        border: 1px solid rgba(180, 120, 255, 0.18);

        box-shadow:
            inset 0 0 18px rgba(180, 120, 255, 0.12),
            0 14px 34px rgba(0, 0, 0, 0.6);

        color: #efe6ff;
        }
    
    .song-infor > div {
        display: flex;
        flex-direction: column;
        gap: 6px;
        }

    .song-infor label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #c9a7ff;
        }
    
    .song-infor input[type="text"] {
        background: #160c2b;
        border: 1px solid rgba(190, 120, 255, 0.25);
        border-radius: 14px;
        padding: 10px 14px;

        color: #f5ecff;
        font-size: 0.9rem;

        outline: none;
        transition:
            border-color 0.2s ease,
            box-shadow 0.2s ease;
        }

    .song-infor input::placeholder {
        color: #9b82c7;
        }
    
    .song-infor input:focus {
        border-color: #c77dff;
        box-shadow:
            0 0 0 2px rgba(199, 125, 255, 0.35),
            0 0 14px rgba(199, 125, 255, 0.3);
        }

    .song-name input,
    .song-artist input {
    font-weight: 500;
    }

</style>