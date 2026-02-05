<script lang="ts">

</script>

<section class="scratch">
    <h3>Scratch</h3>

    <textarea
        class="scratch-input"
        placeholder="Drop a line, an image, a thought…"
    ></textarea>

    <button class="scratch-save">
        Save idea
    </button>

    <div class="scratch-history">
        <h4>Older ideas</h4>

        <!-- example items -->
        <p>“city lights feel like static in my veins”</p>
        <p>“hook about absence”</p>
        <p>“title: no signal, all noise”</p>
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
