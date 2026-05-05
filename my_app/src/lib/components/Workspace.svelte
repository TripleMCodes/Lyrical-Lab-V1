<script lang="ts">
    let {title = $bindable(), artist = $bindable(), album = $bindable(), recent_songs = $bindable(), openStudio} = $props()
</script>

<section class="work-space">
    <h2>Work Space</h2>

    <div class="draft">
        <h3>Draft</h3>
        <span>
            <p>Title</p>
            <p>{title}</p>
        </span>
        <span>
            <p>Artist</p>
            <p>{artist}</p>
        </span>
        <span>
            <p>Album</p>
            <p>{album}</p>
        </span>
        <button onclick={openStudio}>Continue Writing</button>
    </div>

    
    <div class="recent-songs">
        <h3>Recent Songs</h3>
        {#each recent_songs as song }
            <span>
                <p>Title</p>
                <p>{song.song_name || "song name"}</p>
            </span> 
            <span>
                <p>Artist</p>
                <p>{song.song_artist || ""}</p>
            </span> 
            {#if song.album}
                <span>
                    <p>Album</p>
                    <p>{song.song_album || ""}</p>
                </span>
            {/if}
            <span>
                <p>Date Created</p>
                <p>{song.date_created || ""}</p>
            </span> 
            <span>
                <p>Date Modifed</p>
                <p>{song.date_modified || ""}</p>
            </span> 
        {/each}
    </div>
</section>

<style>


/* ========= Workspace shell ========= */
.work-space {
    width: 100%;
    display: grid;
    /* overflow-y: scroll; */
    grid-template-columns: 360px 1fr;
    /* gap: 1.2rem; */
    align-items: start;

    padding: 1rem;

    background: linear-gradient(
        180deg,
        rgba(120, 50, 180, 0.10),
        rgba(25, 8, 40, 0.18)
    );

    border: 1px solid rgba(168, 85, 247, 0.12);
    border-radius: 22px;

    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
}

button{
    margin-top: 1rem;
    padding: 0.6rem 1.2rem;

    background: linear-gradient(145deg, #1e002c, #290038);
    border: 1px solid rgba(180, 120, 255, 0.18);
    border-radius: 12px;

    box-shadow:
        inset 0 0 12px rgba(180, 120, 255, 0.12),
        0 8px 20px rgba(0, 0, 0, 0.4);

    color: #efe6ff;
    font-weight: 600;
    cursor: pointer;
}

/* Title */
.work-space > h2 {
    grid-column: 1 / -1;
    margin: 0;

    font-size: 1.25rem;
    font-weight: 600;
    letter-spacing: 0.04em;

    color: rgba(233, 213, 255, 0.95);
    text-transform: uppercase;
    margin-bottom: 0;
    padding: 0;
}

/* ========= Shared card style ========= */
.draft, .recent-songs {
    position: relative;
    overflow-y: scroll;
    background: linear-gradient(
        180deg,
        rgba(120, 50, 180, 0.25),
        rgba(30, 10, 45, 0.62)
    );

    border: 1px solid rgba(168, 85, 247, 0.22);
    border-radius: 18px;

    padding: 1.2rem 1.2rem;

    box-shadow:
        0 0 26px rgba(168, 85, 247, 0.14),
        inset 0 0 0 1px rgba(255, 255, 255, 0.03);

    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    /* overflow: hidden; */
    max-height: 100%;
}

.recent-songs, .draft{
    overflow-y:scroll ;
    max-height: 280px;
    scrollbar-width: thin;
    scrollbar-color: transparent transparent;
}
.recent-songs::-webkit-scrollbar{
    width:2px;
}

.recent-songs::-webkit-scrollbar-track{
    background: rgba(20, 0, 40, 0.6);
    border-radius: 8px;
}

.recent-songs::-webkit-scrollbar-thumb {
        background: linear-gradient(
            180deg,
            #c77dff,
            #7b2cbf
        );
        border-radius: 8px;
        box-shadow: 0 0 8px rgba(199, 125, 255, 0.6);
        }    

.recent-songs::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(
            180deg,
            #e0aaff,
            #9d4edd
        );
        }



/* Subtle neon edge accent */
.draft::before,
.recent-songs::before {
    content: "";
    position: absolute;
    top: 14px;
    left: 14px;
    width: 10px;
    height: 10px;
    border-radius: 999px;
    background: rgba(168, 85, 247, 0.9);
    box-shadow: 0 0 14px rgba(168, 85, 247, 0.6);
    opacity: 0.55;
}

/* Card titles */
.draft > h3,
.recent-songs > h3 {
    margin: 0 0 0.9rem 0;
    padding-left: 1rem;

    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 0.03em;

    color: rgba(233, 213, 255, 0.92);
}

/* ========= Key-value rows ========= */
.draft > span,
.recent-songs > span {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 1rem;

    padding: 0.55rem 0;

    border-bottom: 1px solid rgba(168, 85, 247, 0.12);
}

.draft > span:last-child {
    border-bottom: none;
}

/* The <p> inside spans */
.draft > span p,
.recent-songs > span p {
    margin: 0;
}

/* Label */
.draft > span p:first-child,
.recent-songs > span p:first-child {
    font-size: 0.82rem;
    color: rgba(233, 213, 255, 0.7);
    letter-spacing: 0.02em;
}

/* Value */
.draft > span p:last-child,
.recent-songs > span p:last-child {
    font-size: 0.95rem;
    font-weight: 600;

    color: rgba(245, 233, 255, 0.98);
    text-shadow: 0 0 6px rgba(168, 85, 247, 0.25);

    max-width: 65%;
    text-align: right;

    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* ========= Recent songs list readability ========= */
.recent-songs {
    display: block;
}

.recent-songs > span {
    border-bottom: 1px solid rgba(168, 85, 247, 0.10);
}


.recent-songs > span:nth-child(5n) {
    margin-bottom: 0.8rem;
    border-bottom: 1px solid rgba(168, 85, 247, 0.22);
}

/* Hover micro-glow */
.draft:hover,
.recent-songs:hover {
    box-shadow:
        0 0 36px rgba(168, 85, 247, 0.20),
        inset 0 0 0 1px rgba(255, 255, 255, 0.05);
}

/* ========= Responsive ========= */
@media (max-width: 960px) {
    .work-space {
        grid-template-columns: 1fr;
    }

    .draft > span p:last-child,
    .recent-songs > span p:last-child {
        max-width: 58%;
    }
}
</style>
