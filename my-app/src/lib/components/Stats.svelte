<script lang="ts">
    let {writing_time = $bindable(), writing_sessions = $bindable(), new_songs = $bindable(), num_songs = $bindable()} = $props()
</script>


<section class="stats">
    <h2>Stats</h2>

    <div class="stat-row">
        <span class="label">Total writing time</span>
        <span class="value">{writing_time}</span>
    </div>

    <div class="stat-row">
        <span class="label">Total songs</span>
        <span class="value">{num_songs}</span>
    </div>

    <div class="stat-row">
        <span class="label">Writing sessions</span>
        <span class="value">{writing_sessions}</span>
    </div>

    <div class="stat-row">
        <span class="label">New songs</span>
        <span class="value">{new_songs}</span>
    </div>
</section>

<style>
.stats {
    width: 100%;
    max-width: 520px;

    background: linear-gradient(
        180deg,
        rgba(120, 50, 180, 0.28),
        rgba(30, 10, 45, 0.6)
    );

    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);

    border-radius: 20px;
    border: 1px solid rgba(168, 85, 247, 0.25);

    box-shadow:
        0 0 28px rgba(168, 85, 247, 0.18),
        inset 0 0 0 1px rgba(255, 255, 255, 0.04);

    padding: 1.6rem 1.8rem;

    color: #f5e9ff;
}

/* Title */
.stats h2 {
    margin: 0 0 1.2rem 0;
    font-size: 1.2rem;
    font-weight: 600;
    letter-spacing: 0.05em;

    color: #e9d5ff;
    text-transform: uppercase;
}

/* Rows */
.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;

    padding: 0.6rem 0;

    border-bottom: 1px solid rgba(168, 85, 247, 0.12);
}

.stat-row:last-child {
    border-bottom: none;
}

/* Labels */
.label {
    font-size: 0.85rem;
    color: rgba(233, 213, 255, 0.7);
    letter-spacing: 0.02em;
}

/* Values */
.value {
    font-size: 1rem;
    font-weight: 600;

    color: #f5e9ff;
    text-shadow: 0 0 6px rgba(168, 85, 247, 0.35);
}
</style>



