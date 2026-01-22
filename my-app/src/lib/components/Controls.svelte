<script>
    import Tooltip from "./Tooltip.svelte"
    let { onSave, selected = $bindable(), searchWord = $bindable(), word = $bindable(), checkFlow, selectedValue = $bindable(), handleChange, generate, selectedGenre = $bindable(), handleGenreChange, selectedFos=$bindable(), handleFosChange, genInput = $bindable()} = $props();
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

            <button onclick={generate}>Generate lyrics</button>
        </div>

        <div>

        </div> 
    </section>

    <section class="r-n-l" >
        <label for="r-n-l">Rhymes and Lexicon</label>
        <input type="text" name="word" id="word" placeholder="Enter worrd here..." bind:value={word}>
        <select name="search" id="search" bind:value={selected}>
        <option value="rhyme">Rhyme</option>
        <option value="synonym">Synonym</option>
        <option value="related">Related</option>
        <option value="homophone">Homophone</option>
        </select>
        <button onclick={searchWord}>Search</button>
    </section>

    <section class="control-btns">

        <Tooltip text="Save">
            <button onclick={onSave}>
                <img src="/icons8-save-64.png" alt="save icon">
            </button>
        </Tooltip>

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

        <button >
            <Tooltip text="criticise lyrics">
                <img src="/icons8-brain-64.png" alt="criticise icon">
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
        padding: 14px;
        border-radius: 16px;
        border: none;
        background: linear-gradient(
            135deg,
            #9b5cff,
            #d066ff
        );
        color: #140a24;
        font-size: 0.95rem;
        font-weight: 600;
        letter-spacing: 0.05em;
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


</style>