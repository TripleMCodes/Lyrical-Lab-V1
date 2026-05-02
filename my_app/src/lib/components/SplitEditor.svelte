<script>

    let { wordCount = $bindable(), charCount = $bindable(), editor1 = $bindable(), editor2 = $bindable(), selectedText = $bindable() , onSelected, loading = $bindable(), cancelRes, saveDraft} = $props()
    import SigilSpinner from '../../lib/components/SigilSpinner.svelte';
    import {get_url} from '$lib/url_vars/urls_vars'
    // let editor2 = $state("");
    
   
    let debounceTimer;

    $effect(() => {
        const words = editor1.trim() === "" ? 0 : editor1.trim().split(/\s+/).length;
        wordCount = words;
        const chars = editor1.replace(/\s/g, "").length
        charCount = chars
        
        const lines = editor1.split(/\r?\n/);

        if (lines.length === 1 && lines[0] === ""){
            editor2 = "";
            return
        }

        clearTimeout(debounceTimer);

        debounceTimer = setTimeout(async () => {
            try{
                const res = await fetch(
                    `${get_url()}/api/lyric-tools/syllabe-counter`,
                    {
                        method: "POST",
                        credentials: "include", 
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ message: lines })
                    }

                );
                const data = await res.json();
                editor2 = data.message
            } catch (err){
                console.error(err)
            }
        }, 300) //300ms
    })




    let editorA = $state(null);
    let editorB = $state(null);
    let isSyncing = false;
    let isResizing = $state(false);

    function startResize() {
    isResizing = true;
    window.addEventListener("mousemove", resize);
    window.addEventListener("mouseup", stopResize);
  }

    function resize(e) {
        if (!isResizing) return;

        const container = document.querySelector(".writing-section");
        const rect = container.getBoundingClientRect();
        const offsetY = e.clientY - rect.top;
        const percentage = Math.min(
        80,
        Math.max(20, (offsetY / rect.height) * 100)
        );

        //@ts-ignore
        container.style.gridTemplateRows = `${percentage}% 6px auto`;
  }


    function stopResize() {
        isResizing = false;
        window.removeEventListener("mousemove", resize);
        window.removeEventListener("mouseup", stopResize);
    }

    function adjustSplit(delta) {
        const container = document.querySelector(".writing-section");
        // @ts-ignore
        const rows = container.style.gridTemplateRows || "1fr 6px 1fr";
        const [top] = rows.split(" ");

        let value = parseFloat(top);
        value = Math.min(80, Math.max(20, value + delta));
        // @ts-ignore
        container.style.gridTemplateRows = `${value}% 6px auto`;
        }

    function handleDividerKeydown(e) {
        if (e.key === "ArrowUp") adjustSplit(-5);
        if (e.key === "ArrowDown") adjustSplit(5);
    }

    function syncScroll(source, target) {
    if (isSyncing) return;

    isSyncing = true;

    const sourceMax =
      source.scrollHeight - source.clientHeight;
    const targetMax =
      target.scrollHeight - target.clientHeight;

    const ratio =
      sourceMax > 0 ? source.scrollTop / sourceMax : 0;

    target.scrollTop = ratio * targetMax;

    requestAnimationFrame(() => {
      isSyncing = false;
    });
  }

</script>

<div class="writing-section">
    <textarea
    class="editor"
    
    bind:this={editorA}
    bind:value={editor1}
    spellcheck="false"
    onscroll={() => syncScroll(editorA, editorB)}
    onselect={onSelected}
    oninput={saveDraft}
  ></textarea>

  <div
    class="divider"
    role="separator"
    aria-orientation="horizontal"
    tabindex="0"
    onmousedown={startResize}
    onkeydown={handleDividerKeydown}
  ></div>

<!-- onscroll={() => syncScroll(editorB, editorA)} -->

    <div class="textarea-wrapper" >
    {#if loading === false}  
        <div class="html-overlay html-overlay-top editor"  
            bind:this={editorA}>
            {@html editor1}
        </div>
      <textarea
        class="editor"
        bind:value={editor2}
        bind:this={editorB}
        spellcheck="false"
        readonly
        onscroll={(e) => {
          const overlay = document.querySelector('.html-overlay-bottom');
          if (overlay) overlay.scrollTop = e.target.scrollTop;
        }}
      ></textarea>
      {/if}


    {#if loading}
        <SigilSpinner text="Consulting the lexicon…" />
        <div class="cancle">
            <button onclick={cancelRes}>Cancel</button>
        </div>
    {:else if loading === false}  
        <div class="html-overlay html-overlay-bottom editor"  
            bind:this={editorB}>
            {@html editor2}
        </div>
        
    {/if}
    </div>      

</div>



<style>
    textarea{
		max-height: 100%;
		font-size: 2rem;
        max-width: 100%;
        min-height: 10%;
        min-width: 10%;
	}

    .ll-container {
        flex: 1;
        display: flex;

        width: 150%;
        height: 200%;

        padding: 1rem;
        box-sizing: border-box;
        }


     .writing-section {
        flex: 1;
        display: grid;
        grid-template-rows: 1fr 6px 1fr;
        min-height: 0; 
        padding: 1rem;
        border-radius: 12px;

        background: rgba(60, 0, 120, 0.1);
        border: 1px solid rgba(200, 120, 255, 0.35);
        }

    .textarea-wrapper {
        position: relative;
        flex: 1;
        width: 100%;
        height: 100%;
        min-height: 0;
        overflow: hidden;
    }
    
    .textarea-wrapper textarea{
        color: transparent;
        overflow-y: auto;
        overflow-x: hidden;
    }


    .html-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        padding: 1rem;
        border-radius: 10px;
        overflow-y: auto;
        overflow-x: hidden;
        pointer-events: none;
        color: #e6ccff;
        font-size: 1.5rem;
        line-height: 1.5;
        white-space: pre-wrap;
        word-break: break-word;
    }

    .editor {
        flex: 1;
        width: 100%;
        height: 100%;
        min-height: 0;
        resize: none;

        padding: 1rem;
        border-radius: 10px;

        background:
            repeating-linear-gradient(
            to bottom,
            rgba(255, 255, 255, 0.06) 0px,
            rgba(255, 255, 255, 0.06) 1px,
            transparent 1px,
            transparent 2em
            ),
            #0b0014;

        color: #e6ccff;
        font-family: "JetBrains Mono", monospace;
        font-size: 1.5rem;
        line-height: 1.5;

        border: 1px solid rgba(200, 120, 255, 0.35);
        box-shadow: inset 0 0 12px rgba(180, 120, 255, 0.25);

        caret-color: #c77dff;
        animation: caretPulse 1.2s infinite ease-in-out;

        outline: none;
        }

    .editor::-webkit-scrollbar {
        width: 10px;
        }

    .editor::-webkit-scrollbar-track {
        background: rgba(20, 0, 40, 0.6);
        border-radius: 8px;
        }

    .editor::-webkit-scrollbar-thumb {
        background: linear-gradient(
            180deg,
            #c77dff,
            #7b2cbf
        );
        border-radius: 8px;
        box-shadow: 0 0 8px rgba(199, 125, 255, 0.6);
        }    

    .editor::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(
            180deg,
            #e0aaff,
            #9d4edd
        );
        }

    .editor {
        scrollbar-width: thin;
        scrollbar-color: #c77dff rgba(20, 0, 40, 0.6);
        }    
    
    .editor:not(:focus) {
        background:
            repeating-linear-gradient(
            to bottom,
            rgba(255, 255, 255, 0.0) 0px,
            rgba(255, 255, 255, 0.0) 1px,
            transparent 1px,
            transparent 1.6em
            ),
            #0b0014;
        }
    
    .divider {
        cursor: row-resize;
        background: linear-gradient(
            90deg,
            transparent,
            #c77dff,
            transparent
        );
        box-shadow: 0 0 10px rgba(199, 125, 255, 0.6);
        }
    
    @keyframes caretPulse {
        0% {
            caret-color: #c77dff;
        }
        50% {
            caret-color: #ff9cff;
        }
        100% {
            caret-color: #c77dff;
        }
        }

    .editor:focus {
        border-color: #c77dff;
        box-shadow:
            inset 0 0 18px rgba(199, 125, 255, 0.35),
            0 0 10px rgba(199, 125, 255, 0.35);
        }

    .editor:not(:focus) {
        animation: none;
        }

    .cancle {
        position: absolute;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%);
        z-index: 10;
    }

    .cancle button {
        padding: 0.75rem 1.5rem;
        background: linear-gradient(135deg, #c77dff, #7b2cbf);
        color: #fff;
        border: 1px solid rgba(199, 125, 255, 0.6);
        border-radius: 6px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 0 15px rgba(199, 125, 255, 0.4);
        transition: all 0.3s ease;
        font-family: inherit;
    }

    .cancle button:hover {
        background: linear-gradient(135deg, #e0aaff, #9d4edd);
        box-shadow: 0 0 25px rgba(199, 125, 255, 0.7);
        transform: translateY(-2px);
    }

    .cancle button:active {
        transform: translateY(0);
        box-shadow: 0 0 12px rgba(199, 125, 255, 0.5);
    }

    /* =========================================
   MEDIA QUERIES — Writing / Editor Component
   xs: < 375px  |  sm: 375–639px  |  md: 640–1023px
   lg: 1024–1279px  |  xl: 1280+  |  2xl: 1600+
   ========================================= */

/* -----------------------------------------
   XS — Very small phones (< 375px)
   ----------------------------------------- */
@media (max-width: 374px) {
  /* .ll-container {
    width: 100%;
    height: 200dvh;         
     padding: 0.5rem;
  }  */

  .writing-section {
    grid-template-rows: 10fr 4px 2fr;  /* Thinner divider on tiny screens */
    padding: 0.5rem;
    border-radius: 8px;
    height: 200%;
    /* min-height: 0; */
    /* width: 200%; */
  }

  textarea {
    font-size: 1rem;         /* 2rem is too large for xs — line wrapping gets painful */
    /* min-height: 80px; */
  }

  .editor {
    font-size: 0.9rem;
    line-height: 1.5;
    padding: 0.6rem;
    border-radius: 8px;
    /* Lined background scaled to match new font size */
    background:
      repeating-linear-gradient(
        to bottom,
        rgba(255, 255, 255, 0.06) 0px,
        rgba(255, 255, 255, 0.06) 1px,
        transparent 1px,
        transparent 1.5em
      ),
      #0b0014;
      /* height: 200%; */
  }

  .html-overlay {
    font-size: 0.9rem;
    line-height: 1.5;
    padding: 0.6rem;
    border-radius: 8px;
  }

  .editor::-webkit-scrollbar {
    width: 5px;              /* Thinner scrollbar on tiny screens */
  }

  .divider {
    cursor: row-resize;      /* Keep functional — touch users can still drag */
    height: 4px;
  }

  .cancle {
    bottom: 1rem;
  }

  .cancle button {
    padding: 0.55rem 1rem;
    font-size: 0.85rem;
  }
}

/* -----------------------------------------
   SM — Standard phones (375px – 639px)
   ----------------------------------------- */
@media (min-width: 375px) and (max-width: 639px) {
  /* .ll-container {
    flex: none;
    width: 100%;
    height: 500dvh;
    padding: 0.75rem;
  } */

  .writing-section {
    grid-template-rows: 10fr 5px 2fr;
    padding: 0.75rem;
    border-radius: 10px;
    height: 400%;
    /* width: 400%; */
  }

  textarea {
    font-size: 1.1rem;
    min-height: 100px;
  }

  .editor {
    font-size: 1rem;
    line-height: 1.5;
    padding: 0.75rem;
    border-radius: 8px;
    background:
      repeating-linear-gradient(
        to bottom,
        rgba(255, 255, 255, 0.06) 0px,
        rgba(255, 255, 255, 0.06) 1px,
        transparent 1px,
        transparent 1.5em
      ),
      #0b0014;
    height: 200%;
  }

  .html-overlay {
    font-size: 1rem;
    line-height: 1.5;
    padding: 0.75rem;
  }

  .editor::-webkit-scrollbar {
    width: 6px;
  }

  .cancle {
    bottom: 1.25rem;
  }

  .cancle button {
    padding: 0.65rem 1.25rem;
    font-size: 0.9rem;
  }
}

/* -----------------------------------------
   MD — Large phones / small tablets (640px – 1023px)
   ----------------------------------------- */
@media (min-width: 640px) and (max-width: 1023px) {
  .ll-container {
    width: 100%;
    height: 100dvh;
    padding: 0.875rem;
  }

  .writing-section {
    grid-template-rows: 10fr 5px 2fr;
    padding: 0.875rem;
    border-radius: 10px;
  }

  textarea {
    font-size: 1.25rem;
  }

  .editor {
    font-size: 1.15rem;
    line-height: 1.5;
    padding: 0.875rem;
    background:
      repeating-linear-gradient(
        to bottom,
        rgba(255, 255, 255, 0.06) 0px,
        rgba(255, 255, 255, 0.06) 1px,
        transparent 1px,
        transparent 1.725em   /* 1.15rem × 1.5 line-height */
      ),
      #0b0014;
  }

  .html-overlay {
    font-size: 1.15rem;
    padding: 0.875rem;
  }

  .cancle button {
    padding: 0.7rem 1.4rem;
  }
}

/* -----------------------------------------
   LG — Tablets / small laptops (1024px – 1279px)
   ----------------------------------------- */
@media (min-width: 1024px) and (max-width: 1279px) {
  /* .ll-container {
    width: 125%;             
    height: 175%;
    padding: 0.875rem;
  } */

  .editor {
    font-size: 1.3rem;
    background:
      repeating-linear-gradient(
        to bottom,
        rgba(255, 255, 255, 0.06) 0px,
        rgba(255, 255, 255, 0.06) 1px,
        transparent 1px,
        transparent 1.95em   /* 1.3rem × 1.5 */
      ),
      #0b0014;
      height: 200%;
  }

  .html-overlay {
    font-size: 1.3rem;
  }

  textarea {
    font-size: 1.65rem;
  }
}

/* -----------------------------------------
   XL — Standard desktops (1280px – 1599px)
   ----------------------------------------- */
@media (min-width: 1280px) {
  /* Base styles are tuned for this range.
     width: 150%, height: 200%, font-size: 1.5rem
     are all intentional — preserved. */

  .editor {
    font-size: 1.5rem;      /* Matches your base */
    background:
      repeating-linear-gradient(
        to bottom,
        rgba(255, 255, 255, 0.06) 0px,
        rgba(255, 255, 255, 0.06) 1px,
        transparent 1px,
        transparent 2.25em   /* 1.5rem × 1.5 */
      ),
      #0b0014;
  }
}

/* -----------------------------------------
   2XL — Large / wide monitors (1600px+)
   ----------------------------------------- */
@media (min-width: 1600px) {
  .ll-container {
    padding: 1.25rem;
  }

  .writing-section {
    padding: 1.25rem;
    border-radius: 14px;
    grid-template-rows: 1fr 8px 1fr;  /* Slightly thicker divider — easier to grab */
  }

  textarea {
    font-size: 2.25rem;
  }

  .editor {
    font-size: 1.75rem;
    line-height: 1.55;
    padding: 1.25rem;
    border-radius: 12px;
    background:
      repeating-linear-gradient(
        to bottom,
        rgba(255, 255, 255, 0.06) 0px,
        rgba(255, 255, 255, 0.06) 1px,
        transparent 1px,
        transparent 2.7125em  /* 1.75rem × 1.55 */
      ),
      #0b0014;
  }

  .html-overlay {
    font-size: 1.75rem;
    line-height: 1.55;
    padding: 1.25rem;
    border-radius: 12px;
  }

  .editor::-webkit-scrollbar {
    width: 12px;
  }

  .cancle {
    bottom: 2.5rem;
  }

  .cancle button {
    padding: 0.875rem 1.75rem;
    font-size: 1.1rem;
  }
}

</style>
