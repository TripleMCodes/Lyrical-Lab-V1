<script>
    let {filters = $bindable(), genres, moods, albums, resetFilters } = $props()
</script>


<section class="filters">
    <h3>Filter Songs</h3>
    <div class="filter-controls">
        <div class="filter-group">
            <label for="genre">Genre</label>
            <select id="genre" bind:value={filters.genre}>
                <option value="">All Genres</option>
                {#each genres as genre}
                    <option value={genre}>{genre}</option>
                {/each}
            </select>
        </div>

        <div class="filter-group">
            <label for="mood">Mood</label>
            <select id="mood" bind:value={filters.mood}>
                <option value="">All Moods</option>
                {#each moods as mood}
                    <option value={mood}>{mood}</option>
                {/each}
            </select>
        </div>

        <div class="filter-group">
            <label for="album">Album</label>
            <select id="album" bind:value={filters.album}>
                <option value="">All Albums</option>
                {#each albums as album}
                    <option value={album}>{album}</option>
                {/each}
            </select>
        </div>

        <div class="filter-group">
            <label for="dateFrom">From Date</label>
            <input id="dateFrom" type="date" bind:value={filters.dateFrom} />
        </div>

        <div class="filter-group">
            <label for="dateTo">To Date</label>
            <input id="dateTo" type="date" bind:value={filters.dateTo} />
        </div>

        <button onclick={resetFilters} class="reset-btn">Reset Filters</button>
    </div>
</section>

<style>
    .filters {
    background: rgba(20, 0, 40, 0.55);
    border: 1px solid rgba(199, 125, 255, 0.35);
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 2rem;

    box-shadow:
        inset 0 0 18px rgba(180, 120, 255, 0.12),
        0 0 20px rgba(120, 60, 255, 0.18);
}

.filters h3 {
    color: #f2d9ff;
    font-size: 1.25rem;
    margin-bottom: 1rem;
    letter-spacing: 0.5px;
    text-shadow: 0 0 8px rgba(199, 125, 255, 0.6);
}


.filter-controls {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    align-items: flex-end;
}

.filter-group {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    min-width: 160px;
}

.filter-group label {
    font-size: 0.8rem;
    color: #d8b4ff;
    letter-spacing: 0.4px;
}

.filter-group select,
.filter-group input[type="date"] {
    background: #0b0014;
    color: #e6ccff;
    border: 1px solid rgba(199, 125, 255, 0.35);
    border-radius: 8px;
    padding: 0.45rem 0.6rem;
    font-size: 0.9rem;
    font-family: inherit;

    box-shadow: inset 0 0 10px rgba(180, 120, 255, 0.15);
    transition: all 0.2s ease;
}

.filter-group select:hover,
.filter-group input:hover {
    border-color: rgba(224, 170, 255, 0.6);
}

.filter-group select:focus,
.filter-group input:focus {
    outline: none;
    border-color: #c77dff;
    box-shadow:
        inset 0 0 14px rgba(199, 125, 255, 0.35),
        0 0 8px rgba(199, 125, 255, 0.35);
}


.reset-btn {
    background: linear-gradient(135deg, #c77dff, #7b2cbf);
    color: #fff;
    border: 1px solid rgba(199, 125, 255, 0.6);
    border-radius: 8px;
    padding: 0.55rem 1.2rem;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;

    box-shadow: 0 0 16px rgba(199, 125, 255, 0.45);
    transition: all 0.25s ease;
}

.reset-btn:hover {
    background: linear-gradient(135deg, #e0aaff, #9d4edd);
    box-shadow: 0 0 26px rgba(199, 125, 255, 0.7);
    transform: translateY(-1px);
}

.reset-btn:active {
    transform: translateY(0);
    box-shadow: 0 0 14px rgba(199, 125, 255, 0.5);
}
</style>
