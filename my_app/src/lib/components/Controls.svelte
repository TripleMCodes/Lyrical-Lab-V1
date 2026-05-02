<script>
    import Tooltip from "./Tooltip.svelte"
    let { onSave, selected = $bindable(), searchWord = $bindable(), word = $bindable(), checkFlow, selectedValue = $bindable(), handleChange, generate, selectedGenre = $bindable(), handleGenreChange, selectedFos=$bindable(), handleFosChange, genInput = $bindable(), createNewSong} = $props();
</script>


<div class="controls-section">
    <section class="l-n-fos-gen">
       <label for="l-n-fos-gen">Lyrics and Figure of speech</label>
        <div class="lyrics-gen">
            <input type="text" placeholder="Enter prompt..." bind:value={genInput}/>

            <div class="configs">
                <select name="genres" id="lyrics" bind:value={selectedGenre} onchange={handleGenreChange}>
                <option value="pop" >Pop</option>
                <option value="rnb">RnB</option>
                <option value="rock">Rock</option>
                <option value="hip-pop">Hip-Pop</option>
                </select>

                <select name="figure-of-speech" id="figure-of-speech" bind:value={selectedFos} onchange={handleFosChange}>
                <option value="simile">Simile</option>
                <option value="metaphor">Metaphor</option>
                <option value="phrase">Phrase</option>
                <option value="idiom">Idiom</option>
                </select>
            </div>

            <div class="mode">
                <span>lyrics gen mode: <input type="radio" name="mode" id="gen-lyrics" value="gen-lyrics" bind:group={selectedValue} onclick={handleChange}/></span>
                <span>Figure of speech mode: <input type="radio" name="mode" id="gen-fos" value="gen-fos" bind:group={selectedValue} onclick={handleChange}/></span>
            </div>
            <button onclick={generate}>
                <Tooltip text="Generate lyrics">
                    <img src="/icons8-lyrics-50.png" alt="lyrics icon">
                </Tooltip>
            </button>
            
        </div>

        <div>

        </div> 
    </section>

    <div class="r-n-l-container">
    <section class="r-n-l" >
        <label for="r-n-l">Rhymes and Lexicon</label>
        <input type="text" name="word" id="word" placeholder="Enter worrd here..." bind:value={word}>
        <select name="search" id="search" bind:value={selected}>
        <option value="rhyme">Rhyme</option>
        <option value="synonym">Synonym</option>
        <option value="related">Related</option>
        <option value="homophone">Homophone</option>
        </select>
        <button onclick={searchWord}>
            <Tooltip text="Search">
                <img src="/icons8-find-64.png" alt="search icon" height="50" width="50">
            </Tooltip>
        </button>
    </section>
    </div>

    <section class="control-btns">

        <button onclick={onSave}>
            <Tooltip text="Save">
                <img src="/icons8-save-64.png" alt="save icon">
            </Tooltip>
        </button>

        <button>
            <Tooltip text="Theme">
                <img src="/icons8-dark-mode-48.png" alt="theme icon">
            </Tooltip>
        </button>

        <button onclick={checkFlow}>
            <Tooltip text="Flow check">
                <img src="/icons8-foursquare-64.png" alt="flow check icon">
            </Tooltip>
        </button>

        <!-- <button >
            <Tooltip text="criticise lyrics">
                <img src="/icons8-brain-64.png" alt="criticise icon">
            </Tooltip>
        </button>  -->

        <button onclick={createNewSong}>
            <Tooltip text="Create new song">
                <img src="/icons8-add-file-64.png" alt="new song icon">
            </Tooltip>
        </button> 
    </section>

</div>


<style>
    .l-n-fos-gen {
        background: radial-gradient(
            120% 120% at top right,
            rgba(160, 90, 255, 0.12),
            transparent 40%
            ),
            linear-gradient(145deg, #0a0614, #12091f);
        border: 1px solid rgba(190, 120, 255, 0.18);
        border-radius: 18px;
        padding: 24px;
        max-width: 640px;
        color: #efe6ff;
        box-shadow:
            0 0 0 1px rgba(180, 120, 255, 0.06),
            0 25px 50px rgba(0, 0, 0, 0.7);
        font-family: system-ui, -apple-system, sans-serif;
        }

    .l-n-fos-gen label {
        font-size: 0.85rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #c8a7ff;
        margin-bottom: 14px;
        display: block;
        }

    .lyrics-gen {
        display: flex;
        flex-direction: column;
        gap: 16px;
        }
    
    .lyrics-gen input[type="text"],
    .lyrics-gen input[type="Enter prompt"] {
    background: #160c2b;
    border: 1px solid rgba(190, 120, 255, 0.25);
    border-radius: 14px;
    padding: 14px 16px;
    color: #f5ecff;
    font-size: 0.95rem;
    outline: none;
    transition: border 0.2s ease, box-shadow 0.2s ease;
    }

    .lyrics-gen input::placeholder {
        color: #9a7fc9;
        }

    .lyrics-gen input:focus {
        border-color: #c77dff;
        box-shadow:
            0 0 0 2px rgba(199, 125, 255, 0.35),
            0 0 18px rgba(199, 125, 255, 0.25);
        }

    .configs {
        display: flex;
        gap: 12px;
        }
    
    .configs select {
        flex: 1;
        background: #160c2b;
        border: 1px solid rgba(190, 120, 255, 0.22);
        border-radius: 14px;
        padding: 12px 14px;
        color: #efe6ff;
        font-size: 0.9rem;
        cursor: pointer;
        } 

    .configs select:focus {
        outline: none;
        border-color: #d18bff;
        box-shadow: 0 0 12px rgba(209, 139, 255, 0.3);
        }

    .mode {
        display: flex;
        justify-content: space-between;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(190, 120, 255, 0.15);
        border-radius: 16px;
        padding: 12px 16px;
        }
    
    .mode span {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.85rem;
        color: #dbc9ff;
        }

    .mode input[type="radio"] {
        accent-color: #c77dff;
        cursor: pointer;
        }

    .lyrics-gen button, button {
        margin-top: 10px;
        padding: 7px;
        border-radius: 16px;
        border: none;
        background: linear-gradient(
            135deg,
            #9b5cff,
            #d066ff
        );
        cursor: pointer;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        }

    .lyrics-gen button:hover {
        transform: translateY(-1px);
        box-shadow:
            0 12px 28px rgba(180, 90, 255, 0.45),
            0 0 0 1px rgba(220, 160, 255, 0.5);
        }

    .lyrics-gen button:active {
        transform: translateY(0);
        box-shadow:
            0 6px 14px rgba(140, 70, 200, 0.4);
        }

    .controls-section {
        flex: 0 0 28%;
        display: flex;
        flex-direction: column;
        gap: 0.75rem;

        padding: 1rem;
        border-radius: 12px;

        background: rgba(120, 0, 255, 0.08);
        border: 1px solid rgba(180, 120, 255, 0.25);
        box-shadow: inset 0 0 12px rgba(180, 120, 255, 0.15);
        }

    .r-n-l {
        background: linear-gradient(145deg, #0a0614, #12091f);
        border: 1px solid rgba(190, 120, 255, 0.18);
        border-radius: 18px;
        padding: 24px;
        max-width: 500px;
        display: flex;
        flex-direction: column;
        gap: 16px;
        color: #efe6ff;
        box-shadow:
            0 0 0 1px rgba(180, 120, 255, 0.06),
            0 20px 40px rgba(0, 0, 0, 0.6);
        font-family: system-ui, -apple-system, sans-serif;
        }

    .r-n-l label {
        font-size: 0.85rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #c8a7ff;
        margin-bottom: 8px;
        display: block;
        }

    .r-n-l input[type="text"] {
        background: #160c2b;
        border: 1px solid rgba(190, 120, 255, 0.25);
        border-radius: 14px;
        padding: 12px 16px;
        color: #f5ecff;
        font-size: 0.95rem;
        outline: none;
        transition: border 0.2s ease, box-shadow 0.2s ease;
        } 

    .r-n-l input::placeholder {
        color: #9a7fc9;
        }

    .r-n-l input:focus {
        border-color: #c77dff;
        box-shadow:
            0 0 0 2px rgba(199, 125, 255, 0.35),
            0 0 12px rgba(199, 125, 255, 0.25);
        }

    .r-n-l select {
        background: #160c2b;
        border: 1px solid rgba(190, 120, 255, 0.22);
        border-radius: 14px;
        padding: 12px 14px;
        color: #efe6ff;
        font-size: 0.9rem;
        cursor: pointer;
        transition: border 0.2s ease, box-shadow 0.2s ease;
        }
    
    .r-n-l select:focus {
        outline: none;
        border-color: #d18bff;
        box-shadow: 0 0 12px rgba(209, 139, 255, 0.3);
        }
    
    .r-n-l button {
        padding: 14px;
        border-radius: 16px;
        border: none;
        background: linear-gradient(135deg, #9b5cff, #d066ff);
        color: #140a24;
        font-size: 0.95rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        cursor: pointer;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
    
    .r-n-l button:hover {
        transform: translateY(-1px);
        box-shadow:
            0 12px 28px rgba(180, 90, 255, 0.45),
            0 0 0 1px rgba(220, 160, 255, 0.5);
        }

    .r-n-l button:active {
        transform: translateY(0);
        box-shadow:
            0 6px 14px rgba(140, 70, 200, 0.4);
        }

    .control-btns {
        display: flex;
        gap: 12px;
        padding: 12px;
        border-radius: 16px;

        background: linear-gradient(145deg, #0b0518, #140a26);
        border: 1px solid rgba(180, 120, 255, 0.18);

        box-shadow:
            inset 0 0 16px rgba(180, 120, 255, 0.12),
            0 10px 30px rgba(0, 0, 0, 0.55);

        align-items: center;
        justify-content: center;
        }

    .control-btns button {
        width: 48px;
        height: 48px;
        border-radius: 14px;
        border: 1px solid rgba(190, 120, 255, 0.22);

        background: radial-gradient(
            circle at top left,
            #1b0f33,
            #0d061b
        );

        display: flex;
        align-items: center;
        justify-content: center;

        cursor: pointer;
        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease,
            border-color 0.15s ease;
        }

    .control-btns button img {
        width: 22px;
        height: 22px;
        filter:
            invert(87%)
            sepia(23%)
            saturate(1450%)
            hue-rotate(235deg);
        pointer-events: none;
        }

    .control-btns button:hover {
        transform: translateY(-2px);
        border-color: #c77dff;
        box-shadow:
            0 0 0 1px rgba(199, 125, 255, 0.4),
            0 10px 24px rgba(199, 125, 255, 0.45);
        }

    .control-btns button:active {
        transform: translateY(0);
        box-shadow:
            inset 0 0 14px rgba(160, 90, 255, 0.45);
        }

    .control-btns button:focus-visible {
        outline: none;
        box-shadow:
            0 0 0 2px rgba(210, 160, 255, 0.6),
            0 0 18px rgba(210, 160, 255, 0.45);
        }

    .controls-section {
        transition: width 0.25s ease, padding 0.25s ease;
    }

    /* =========================================
   MEDIA QUERIES — Lyrics Generator & Controls
   xs: < 375px  |  sm: 375–639px  |  md: 640–1023px
   lg: 1024–1279px  |  xl: 1280+  |  2xl: 1600+
   ========================================= */

/* -----------------------------------------
   XS — Very small phones (< 375px)
   ----------------------------------------- */
@media (max-width: 374px) {
  .l-n-fos-gen {
    /* padding: 14px; */
    display: flex;
    flex-direction: column;
    /* justify-content: center; */
    /* align-items: center; */
    border-radius: 12px;
    width: 100%;
  }

  .l-n-fos-gen label {
    font-size: 0.72rem;
    margin-bottom: 8px;
  }

  .lyrics-gen {
    gap: 10px;
  }

  .lyrics-gen input[type="text"],
  .lyrics-gen input[type="Enter prompt"] {
    padding: 10px 12px;
    font-size: 0.85rem;
    border-radius: 10px;
  }

  /* Stack selects vertically — too cramped side by side */
  .configs {
    flex-direction: column;
    gap: 8px;
  }

  .configs select {
    font-size: 0.82rem;
    padding: 10px 12px;
    border-radius: 10px;
  }

  /* Stack mode radio options vertically */
  .mode {
    flex-direction: column;
    gap: 8px;
    padding: 10px 12px;
    border-radius: 12px;
  }

  .mode span {
    font-size: 0.78rem;
  }

  .lyrics-gen button {
    padding: 10px;
    border-radius: 12px;
    font-size: 0.85rem;
  }

  /* Controls sidebar becomes full-width bar at bottom */
  .controls-section {
    flex: 0 0 auto;
    flex-direction: row;        /* Horizontal on mobile */
    flex-wrap: wrap;
    gap: 0.5rem;
    padding: 0.75rem;
    border-radius: 10px;
    width: 100%;
  }

  .control-btns {
    gap: 8px;
    padding: 8px;
    border-radius: 12px;
    flex-wrap: wrap;
    /* justify-content: center; */
    width:100%;
    justify-content: space-evenly;
  }

  .control-btns button {
    width: 40px;
    height: 40px;
    border-radius: 10px;
  }

  .control-btns button img {
    width: 18px;
    height: 18px;
  }

  /* r-n-l panel */
  .r-n-l {
    /* display: none; */
    padding: 14px;
    border-radius: 12px;
    /* flex-direction:row; */
    gap: 10px;
    width:110%;
  }

  .r-n-l label {
    font-size: 0.72rem;
    margin-bottom: 5px;
  }

  .r-n-l input[type="text"] {
    padding: 9px 12px;
    font-size: 0.85rem;
    border-radius: 10px;
  }

  .r-n-l select {
    padding: 9px 12px;
    font-size: 0.82rem;
    border-radius: 10px;
  }

  .r-n-l button {
    padding: 10px;
    font-size: 0.85rem;
    border-radius: 12px;
  }
}

/* -----------------------------------------
   SM — Standard phones (375px – 639px)
   ----------------------------------------- */
@media (min-width: 375px) and (max-width: 639px) {

   .controls-section{
    display: flex;
    flex-direction: column;
    /* justify-content: center;
    align-items: center */
   }

   .r-n-l-container{
    display:flex;
    flex-direction:column;
   }
  .l-n-fos-gen {
    padding: 16px;
    border-radius: 14px;
    width: 100%;
  }

  .l-n-fos-gen label {
    font-size: 0.78rem;
    margin-bottom: 10px;
  }

  .lyrics-gen {
    gap: 12px;
  }

  .lyrics-gen input[type="text"],
  .lyrics-gen input[type="Enter prompt"] {
    padding: 11px 14px;
    font-size: 0.88rem;
    border-radius: 12px;
  }

  /* Configs: allow wrapping but try to stay in a row */
  .configs {
    flex-wrap: wrap;
    gap: 10px;
  }

  .configs select {
    flex: 1 1 45%;            /* Two per row if space allows */
    font-size: 0.85rem;
    padding: 10px 12px;
    border-radius: 12px;
  }

  .mode {
    flex-wrap: wrap;
    gap: 6px;
    padding: 10px 14px;
  }

  .mode span {
    font-size: 0.82rem;
  }

  .lyrics-gen button {
    padding: 11px;
    font-size: 0.9rem;
    border-radius: 14px;
  }

  .controls-section {
    flex: 0 0 auto;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 0.6rem;
    padding: 0.875rem;
    width: 100%;
  }

  .control-btns {
    gap: 10px;
    padding: 10px;
    border-radius: 14px;
    flex-wrap: wrap;
    justify-content: space-evenly;
    width: 100%
  }

  .control-btns button {
    width: 42px;
    height: 42px;
    border-radius: 12px;
  }

  .control-btns button img {
    width: 20px;
    height: 20px;
  }

  .r-n-l {
    /* display:flex; */
    flex-direction: column;
    padding: 16px;
    border-radius: 14px;
    width: 125%;
    gap: 12px;
  }

  .r-n-l label {
    font-size: 0.78rem;
    margin-bottom: 6px;
  }

  .r-n-l input[type="text"] {
    padding: 10px 14px;
    font-size: 0.88rem;
    border-radius: 12px;
  }

  .r-n-l select {
    padding: 10px 12px;
    font-size: 0.85rem;
    border-radius: 12px;
  }

  .r-n-l button {
    padding: 12px;
    font-size: 0.88rem;
  }
}



/* -----------------------------------------
   MD — Large phones / small tablets (640px – 1023px)
   ----------------------------------------- */
@media (min-width: 640px) and (max-width: 1023px) {
  .l-n-fos-gen {
    padding: 18px;
    border-radius: 16px;
    max-width: 100%;
  }

  .lyrics-gen {
    gap: 14px;
  }

  .lyrics-gen input[type="text"],
  .lyrics-gen input[type="Enter prompt"] {
    padding: 12px 14px;
    font-size: 0.9rem;
  }

  .configs {
    gap: 10px;
  }

  .configs select {
    font-size: 0.875rem;
    padding: 11px 13px;
  }

  .mode {
    padding: 11px 14px;
  }

  /* Controls sidebar: narrow column beside main content */
  .controls-section {
    flex: 0 0 22%;            /* Slightly narrower than the 28% base */
    gap: 0.65rem;
    padding: 0.875rem;
  }

  .control-btns {
    gap: 10px;
    padding: 10px;
    justify-content: space-evenly;
  }

  .control-btns button {
    width: 44px;
    height: 44px;
  }

  .r-n-l {
    padding: 18px;
    border-radius: 16px;
    max-width: 100%;
    gap: 14px;
  }

  .r-n-l button {
    padding: 13px;
  }
}

/* -----------------------------------------
   LG — Tablets / small laptops (1024px – 1279px)
   ----------------------------------------- */
@media (min-width: 1024px) and (max-width: 1279px) {
  .l-n-fos-gen {
    padding: 20px;
    max-width: 580px;
  }

  .lyrics-gen {
    gap: 15px;
  }

  .configs select {
    font-size: 0.88rem;
  }

  /* controls-section starts returning to its desktop role */
  .controls-section {
    flex: 0 0 25%;
    gap: 0.7rem;
  }

  .control-btns button {
    width: 46px;
    height: 46px;
  }

  .r-n-l {
    padding: 20px;
    max-width: 460px;
    gap: 15px;
  }
}

/* -----------------------------------------
   XL — Standard desktops (1280px – 1599px)
   ----------------------------------------- */
@media (min-width: 1280px) {
  /* Base styles are tuned for this range — preserved. */

  .l-n-fos-gen {
    max-width: 640px;         /* Matches your base */
    padding: 24px;
  }

  .controls-section {
    flex: 0 0 28%;            /* Matches your base */
  }

  .control-btns button {
    width: 48px;              /* Matches your base */
    height: 48px;
  }

  .r-n-l {
    max-width: 500px;         /* Matches your base */
    padding: 24px;
  }
}

/* -----------------------------------------
   2XL — Large / wide monitors (1600px+)
   ----------------------------------------- */
@media (min-width: 1600px) {
  .l-n-fos-gen {
    padding: 30px;
    border-radius: 22px;
    max-width: 720px;
  }

  .l-n-fos-gen label {
    font-size: 0.9rem;
    margin-bottom: 16px;
  }

  .lyrics-gen {
    gap: 20px;
  }

  .lyrics-gen input[type="text"],
  .lyrics-gen input[type="Enter prompt"] {
    padding: 16px 18px;
    font-size: 1rem;
    border-radius: 16px;
  }

  .configs {
    gap: 14px;
  }

  .configs select {
    font-size: 0.95rem;
    padding: 14px 16px;
    border-radius: 16px;
  }

  .mode {
    padding: 14px 18px;
    border-radius: 18px;
  }

  .mode span {
    font-size: 0.9rem;
    gap: 10px;
  }

  .lyrics-gen button {
    padding: 14px;
    border-radius: 18px;
  }

  .controls-section {
    flex: 0 0 26%;            /* Pull in slightly — prevents over-stretch */
    gap: 0.9rem;
    padding: 1.25rem;
    border-radius: 14px;
  }

  .control-btns {
    gap: 14px;
    padding: 14px;
    border-radius: 18px;
  }

  .control-btns button {
    width: 54px;
    height: 54px;
    border-radius: 16px;
  }

  .control-btns button img {
    width: 26px;
    height: 26px;
  }

  .r-n-l {
    padding: 30px;
    border-radius: 22px;
    max-width: 580px;
    gap: 20px;
  }

  .r-n-l label {
    font-size: 0.9rem;
    margin-bottom: 10px;
  }

  .r-n-l input[type="text"] {
    padding: 14px 18px;
    font-size: 1rem;
    border-radius: 16px;
  }

  .r-n-l select {
    padding: 14px 16px;
    font-size: 0.95rem;
    border-radius: 16px;
  }

  .r-n-l button {
    padding: 16px;
    font-size: 1rem;
    border-radius: 18px;
  }
}


</style>