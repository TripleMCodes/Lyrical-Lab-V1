<script>

    let { wordCount = $bindable(), charCount = $bindable(), editor1 = $bindable(), editor2 = $bindable() } = $props()
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
                    "http://localhost:8000/api/lyric-tools/syllabe-counter",
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
        }, 300) //300ms after typing

    })




    let editorA;
    let editorB;
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
  ></textarea>

  <div
    class="divider"
    role="separator"
    aria-orientation="horizontal"
    tabindex="0"
    onmousedown={startResize}
    onkeydown={handleDividerKeydown}
  ></div>


    <textarea
    class="editor"
    bind:value={editor2}
     bind:this={editorB}
     onscroll={() => syncScroll(editorB, editorA)}
    spellcheck="false"
    readonly
  ></textarea>

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

</style>
