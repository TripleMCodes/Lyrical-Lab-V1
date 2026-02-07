<script lang="ts">

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
            Save idea
        </button>
        <button class="scratch-save" onclick={makeNewNote}>
            New Note
        </button>
    </div>

    <div class="scratch-history">
        <h4>Older ideas</h4>

        <!-- example items -->
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
  height: 100px;              /* adjust as needed */
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
    align-self: flex-end;

    background: rgba(168, 85, 247, 0.18);
    border: 1px solid rgba(168, 85, 247, 0.35);
    border-radius: 999px;

    padding: 0.35rem 0.9rem;

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

</style>
