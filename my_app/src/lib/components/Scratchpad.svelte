<script lang="ts">
  import Tooltip from "./Tooltip.svelte";


    let {notes = $bindable(), viewNote, saveNote, delNote, note = $bindable(), makeNewNote} = $props()

</script>

<section class="scratch">
    <h3>Scratch</h3>

    <textarea
        class="scratch-input"
        bind:value={note}
        placeholder="Drop a line, an image, a thought…"
    ></textarea>

    <div class="btn-container">
        <button class="scratch-save" onclick={saveNote}>
            <Tooltip text="Save note">
                <img src="/icons8-save-64.png" alt="save icon" width="50" height="50">
            </Tooltip>
        </button>
        <button class="scratch-save" onclick={makeNewNote}>
           <Tooltip text="Create new note">
                <img src="/icons8-add-file-64.png" alt="new song icon" width="50" height="50">
            </Tooltip>
        </button>
    </div>

    <div class="scratch-history">
        <h4>Older ideas</h4>

        <div class="note-container">
        {#if notes}
            {#each notes as note (note.id)}
            <div class="note-row">
                <input
                type="text"
                value={note.note}
                readonly
                onclick={() => viewNote(note.note, note.id)}
                />
                <button onclick={() => delNote(note.id)}>Delete</button>
            </div>
            {/each}
        {:else}
            <p class="empty">No notes saved yet.</p>
        {/if}
        </div>


        
    </div>
</section>

<style>
    .scratch {
    background: linear-gradient(
        180deg,
        rgba(120, 50, 180, 0.22),
        rgba(30, 10, 45, 0.6)
    );

    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);

    border: 1px solid rgba(168, 85, 247, 0.22);
    border-radius: 18px;

    padding: 1.2rem 1.4rem;

    box-shadow:
        0 0 26px rgba(168, 85, 247, 0.14),
        inset 0 0 0 1px rgba(255, 255, 255, 0.03);

    color: rgba(245, 233, 255, 0.95);

    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}

/* Title */
.scratch h3 {
    margin: 0;
    font-size: 0.95rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: rgba(233, 213, 255, 0.85);
}

/* Writing area */
.scratch-input {
    width: 100%;
    min-height: 90px;
    resize: vertical;

    background: rgba(15, 5, 25, 0.6);
    border: 1px solid rgba(168, 85, 247, 0.18);
    border-radius: 12px;

    padding: 0.8rem 0.9rem;

    color: rgba(245, 233, 255, 0.95);
    font-size: 0.9rem;
    line-height: 1.45;

    outline: none;
}
.btn-container{
    display:flex;
    flex-direction: row;
}
.note-container {
  height: 400px;
  overflow-y: scroll;
  /* padding-right: 0.5rem;          prevents content clipping */
  /* border: 2px solid blanchedalmond;  */
}

/* Firefox */
.note-container {
  scrollbar-width: thin;
  scrollbar-color: transparent transparent;
}

/* WebKit (Chrome, Edge, Safari) */
.note-container::-webkit-scrollbar {
  width: 2%;
}

.note-container::-webkit-scrollbar-track {
  background: transparent;
}

.note-container::-webkit-scrollbar-thumb {
  background-color: transparent;
}

/* Optional: show scrollbar subtly on hover */
.note-container:hover::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.15);
}

/* Note row layout */
.note-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.4rem;
}

/* Input styling */
.note-row input {
  flex: 1;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 6px;
  padding: 0.4rem 0.6rem;
  color: #e5e7eb;
  cursor: pointer;
}

.note-row input:focus {
  outline: none;
}

/* Delete button */
.note-row button {
  background: transparent;
  border: none;
  color: #f87171;
  font-size: 0.85rem;
  cursor: pointer;
}

.note-row button:hover {
  text-decoration: underline;
}

/* Empty state */
.empty {
  color: #9ca3af;
  font-size: 0.85rem;
  padding: 0.5rem 0;
}


.scratch-input::placeholder {
    color: rgba(233, 213, 255, 0.45);
}

.scratch-input:focus {
    border-color: rgba(168, 85, 247, 0.45);
    box-shadow: 0 0 12px rgba(168, 85, 247, 0.25);
}

/* Save button */
.scratch-save {
    align-self: flex-start;

    background: rgba(168, 85, 247, 0.18);
    border: 1px solid rgba(168, 85, 247, 0.35);
    border-radius: 999px;

    padding: 0.35rem 0.9rem;
    margin:0.35rem;

    color: rgba(245, 233, 255, 0.95);
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.04em;
    text-transform: uppercase;

    cursor: pointer;

    transition: all 0.2s ease;
}

.scratch-save:hover {
    background: rgba(168, 85, 247, 0.28);
    box-shadow: 0 0 14px rgba(168, 85, 247, 0.35);
}

/* Older ideas */
.scratch-history {
    margin-top: 0.4rem;
    padding-top: 0.6rem;

    border-top: 1px solid rgba(168, 85, 247, 0.12);
}

.scratch-history h4 {
    margin: 0 0 0.4rem 0;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;

    color: rgba(233, 213, 255, 0.65);
}

.scratch-history p {
    margin: 0.25rem 0;
    font-size: 0.85rem;
    color: rgba(233, 213, 255, 0.85);

    opacity: 0.85;
}

/* =========================================
   MEDIA QUERIES — Scratchpad Component
   xs: < 375px  |  sm: 375–639px  |  md: 640–1023px
   lg: 1024–1279px  |  xl: 1280+  |  2xl: 1600+
   ========================================= */

/* -----------------------------------------
   XS — Very small phones (< 375px)
   ----------------------------------------- */
@media (max-width: 374px) {
  .scratch {
    padding: 0.875rem 1rem;
    border-radius: 12px;
    gap: 0.6rem;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
  }

  .scratch h3 {
    font-size: 0.82rem;
  }

  .scratch-input {
    min-height: 70px;
    font-size: 0.82rem;
    padding: 0.65rem 0.75rem;
    border-radius: 10px;
  }

  .btn-container {
    gap: 0;                   /* Buttons already have margin: 0.35rem */
  }

  .scratch-save {
    padding: 0.25rem 0.65rem;
    font-size: 0.68rem;
  }

  /* Shrink icons — 50px is oversized on xs */
  .scratch-save img {
    width: 36px;
    height: 36px;
  }

  .note-container {
    height: 260px;            /* Shorter — xs screens are shallow */

  }

  .note-container::-webkit-scrollbar {
    width: 3px;
   
  }

  .note-row {
    gap: 0.35rem;
    margin-bottom: 0.3rem;
    /* grid-template-columns: 2fr 1fr; */
    flex-direction: column;
  }

  .note-row input {
    font-size: 0.78rem;
    /* padding: 0.35rem 0.5rem; */
    width: 100%;
  }

  .note-row button {
    /* font-size: 0.75rem; */
    white-space: nowrap;      /* Prevent "Delete" wrapping to two lines */
    margin: 0rem;
    padding:0rem;
  }

  .scratch-history h4 {
    font-size: 0.68rem;
  }

  .scratch-history p,
  .empty {
    font-size: 0.78rem;
  }
}

/* -----------------------------------------
   SM — Standard phones (375px – 639px)
   ----------------------------------------- */
@media (min-width: 375px) and (max-width: 639px) {
  .scratch {
    padding: 1rem 1.1rem;
    border-radius: 14px;
    gap: 0.7rem;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
  }

  .scratch h3 {
    font-size: 0.88rem;
  }

  .scratch-input {
    min-height: 80px;
    font-size: 0.85rem;
    padding: 0.7rem 0.8rem;
    border-radius: 10px;
  }

  .scratch-save img {
    width: 40px;
    height: 40px;
  }

  .note-container {
    height: 300px;
  }

    .note-row{
        flex-direction: column;

    }
  .note-row input {
    font-size: 0.82rem;
  }

  .note-row button {
    font-size: 0.8rem;
    white-space: nowrap;
  }

  .scratch-history h4 {
    font-size: 0.7rem;
  }
}

/* -----------------------------------------
   MD — Large phones / small tablets (640px – 1023px)
   ----------------------------------------- */
@media (min-width: 640px) and (max-width: 1023px) {
  .scratch {
    padding: 1.1rem 1.25rem;
    border-radius: 16px;
    gap: 0.75rem;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
  }

  .scratch h3 {
    font-size: 0.9rem;
  }

  .scratch-input {
    min-height: 85px;
    font-size: 0.875rem;
    padding: 0.75rem 0.85rem;
  }

  .scratch-save img {
    width: 44px;
    height: 44px;
  }

  .note-container {
    height: 340px;
  }

  .note-row input {
    font-size: 0.85rem;
  }
}

/* -----------------------------------------
   LG — Tablets / small laptops (1024px – 1279px)
   ----------------------------------------- */
@media (min-width: 1024px) and (max-width: 1279px) {
  .scratch {
    padding: 1.1rem 1.3rem;
    border-radius: 16px;
    gap: 0.75rem;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
  }

  .scratch-input {
    min-height: 88px;
    font-size: 0.875rem;
  }

  .scratch-save img {
    width: 46px;
    height: 46px;
  }

  .note-container {
    height: 370px;
  }
}

/* -----------------------------------------
   XL — Standard desktops (1280px – 1599px)
   ----------------------------------------- */
@media (min-width: 1280px) {
  /* Base styles are tuned for this range — preserved.
     padding: 1.2rem 1.4rem, border-radius: 18px,
     min-height: 90px, note-container height: 400px
     are all intentional. */

  .scratch-save img {
    width: 50px;              /* Matches base */
    height: 50px;
  }
}

/* -----------------------------------------
   2XL — Large / wide monitors (1600px+)
   ----------------------------------------- */
@media (min-width: 1600px) {
  .scratch {
    padding: 1.5rem 1.75rem;
    border-radius: 22px;
    gap: 1rem;
  }

  .scratch h3 {
    font-size: 1.05rem;
  }

  .scratch-input {
    min-height: 110px;
    font-size: 0.95rem;
    padding: 0.95rem 1rem;
    border-radius: 14px;
  }

  .scratch-save {
    padding: 0.45rem 1.1rem;
    font-size: 0.8rem;
  }

  .scratch-save img {
    width: 56px;
    height: 56px;
  }

  .note-container {
    height: 460px;
  }

  .note-row {
    gap: 0.65rem;
    margin-bottom: 0.5rem;
  }

  .note-row input {
    font-size: 0.9rem;
    padding: 0.5rem 0.75rem;
    border-radius: 8px;
  }

  .note-row button {
    font-size: 0.875rem;
  }

  .scratch-history h4 {
    font-size: 0.8rem;
    margin-bottom: 0.5rem;
  }

  .scratch-history p,
  .empty {
    font-size: 0.9rem;
  }
}

</style>
