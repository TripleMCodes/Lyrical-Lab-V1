<script>
    let { title = $bindable(), artist = $bindable(), album = $bindable(), mood = $bindable(), genre = $bindable() } = $props();
</script>

<section  class="song-infor">
  <div class="song-name">
    <label for="title">Title: </label>
    <input type="text" name="title" id="title" bind:value={title} placeholder="Required">
  </div>

  <div class="song-artist">
    <label for="artist">Artist: </label>
    <input type="text" name="artist" id="artist" bind:value={artist} placeholder="Required">
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
    <input type="text" name="genre" id="genre" placeholder="Required" bind:value={genre}>
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
        justify-content:center;
        /* align-items: center; */
        width: 127%;

        padding: 20px 24px;
        /* padding-bottom: 10px;
        padding-top: 10px; */
        border-radius: 18px;

        background: linear-gradient(145deg, #0b0518, #130a24);
        border: 1px solid rgba(180, 120, 255, 0.18);

        box-shadow:
            inset 0 0 18px rgba(180, 120, 255, 0.12),
            0 14px 34px rgba(0, 0, 0, 0.6);

        color: #efe6ff;
        margin:20px;
        }
    
    .song-infor > div {
        display: flex;
        flex-direction: column;
        /* gap: 6px; */
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
        /* padding: 10px 12px; */
        padding-bottom: 10px;
        padding-top: 10px;
        padding-left: 5px;
        text-align: start;

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

    /* =========================================
   MEDIA QUERIES — Song Info Component
   xs: < 375px  |  sm: 375–639px  |  md: 640–1023px
   lg: 1024–1279px  |  xl: 1280+  |  2xl: 1600+
   ========================================= */

/* -----------------------------------------
   XS — Very small phones (< 375px)
   ----------------------------------------- */
@media (max-width: 374px) {
  section div {
    margin-left: 0.5rem;
    margin-right: 0.5rem;
  }

  .song-infor {
    flex-direction: column;  /* Stack fields vertically */
    width: 95%;
    padding: 12px 14px;
    border-radius: 12px;
    margin: 10px 0;
    gap: 10px;
  }

  .song-infor > div {
    width: 100%;
  }

  .song-infor label {
    font-size: 0.65rem;
    margin-bottom: 3px;
  }

  .song-infor input[type="text"] {
    width: 100%;
    font-size: 0.82rem;
    padding: 8px 10px;
    border-radius: 10px;
  }
}

/* -----------------------------------------
   SM — Standard phones (375px – 639px)
   ----------------------------------------- */
@media (min-width: 375px) and (max-width: 639px) {
  section div {
    margin-left: 0.75rem;
    margin-right: 0.75rem;
  }

  .song-infor {
    flex-direction: column;  /* Still stacked — too cramped side-by-side */
    width: 95%;
    padding: 1rem;
    border-radius: 14px;
    /* margin: 12px 0; */
    gap: 12px;
  }

  .song-infor > div {
    width: 100%;
  }

  .song-infor label {
    font-size: 0.68rem;
    margin-bottom: 4px;
  }

  .song-infor input[type="text"] {
    width: 100%;
    font-size: 0.875rem;
    padding: 9px 10px;
    border-radius: 12px;
  }
}

/* -----------------------------------------
   MD — Large phones / small tablets (640px – 1023px)
   ----------------------------------------- */
@media (min-width: 640px) and (max-width: 1023px) {
  section div {
    margin-left: 1.25rem;
    margin-right: 1.25rem;
  }

  .song-infor {
    flex-direction: row;     /* Fields return to a row at this size */
    flex-wrap: wrap;         /* But wrap gracefully if there are many */
    width: 90%;
    padding: 16px 18px;
    border-radius: 16px;
    margin: 14px 0;
    gap: 12px;
  }

  .song-infor > div {
    flex: 1 1 40%;           /* Each field takes ~half width, wraps if needed */
    min-width: 140px;
  }

  .song-infor label {
    font-size: 0.7rem;
  }

  .song-infor input[type="text"] {
    width: 100%;
    font-size: 0.88rem;
  }
}

/* -----------------------------------------
   LG — Tablets / small laptops (1024px – 1279px)
   ----------------------------------------- */
@media (min-width: 1024px) and (max-width: 1279px) {
  section div {
    margin-left: 1.5rem;
    margin-right: 1.5rem;
    /* flex: 1; */
  }

  

  .song-infor {
    width: 100%;             /* Step down from the 127% base */
    /* padding: 18px 20px; */
    /* margin: 16px; */
    /* gap: 10px; */
  }

  /* .song-infor > div {
    flex: 1 1 auto;
  } */

  .song-name, .song-genre, .song-mood, .song-artist, .song-album {
    margin:0.04rem;
    gap: 4px;
  }

  .song-infor input[type="text"] {
    font-size: 0.88rem;
  }
}

/* -----------------------------------------
   XL — Standard desktops (1280px – 1599px)
   ----------------------------------------- */
@media (min-width: 1280px) {
  /* Base styles are tuned for this range.
     width: 127% is intentional in its parent
     flex context — preserved here. */

  section div {
    margin-left: 2rem;       /* Matches your base */
    margin-right: 2rem;
  }

  .song-infor {
    padding: 20px 24px;
    border-radius: 18px;
    margin: 20px;
  }
}

/* -----------------------------------------
   2XL — Large / wide monitors (1600px+)
   ----------------------------------------- */
@media (min-width: 1600px) {
  section div {
    margin-left: 2.5rem;
    margin-right: 2.5rem;
  }

  .song-infor {
    padding: 24px 30px;
    border-radius: 20px;
    margin: 22px;
    gap: 16px;
  }

  .song-infor label {
    font-size: 0.8rem;
    letter-spacing: 0.1em;
    margin-bottom: 5px;
  }

  .song-infor input[type="text"] {
    font-size: 0.95rem;
    padding: 12px 14px;
    border-radius: 16px;
  }
}

</style>