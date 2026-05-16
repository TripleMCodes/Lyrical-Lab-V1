<script>
  import { fetchWords } from '$lib/api/client'
  import SigilSpinner from '$lib/components/SigilSpinner.svelte';

  let isLoading = $state(false);
  let selected = $state('rhyme')
  let word = $state('')
  let wordList = $state([])
  let phraseList = $state([])
  let notify = $state('No words searched yet')

  async function fetchWordsWrapper() {
    isLoading = true;
    if (selected === "rhyme") {
      try {
        const res = await fetch(`https://m-prosody.onrender.com/api/public/get-rhymes`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ word: word })
        });
        const data = await res.json();
        wordList = data.word_rhymes;
        phraseList = data.phrasal_rhymes;
        word = '';
      } catch (err) {
        const data = { error: 'Request failed' };
      } finally {
        isLoading = false;
      }
    } else {
      const lst = await fetchWords(selected, word);
      wordList = lst;
      if (wordList.length === 0) notify = "No results found";
      word = '';
      isLoading = false;
    }
  }
</script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

  :global(*, *::before, *::after) { box-sizing: border-box; margin: 0; padding: 0; }

  :global(body) {
    font-family: 'DM Sans', sans-serif;
    background: #FAF9F6;
    color: #1a1a18;
  }

  /* ── HEADER ── */
  .site-header {
    background: #1B3280;
    height: 72px;
    display: flex;
    align-items: center;
    padding: 0 3rem;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
  }

  .logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    color: #fff;
    letter-spacing: 0.02em;
    font-style: italic;
  }

  .logo span {
    font-style: normal;
    font-weight: 600;
    color: #a8bfff;
  }

  nav {
    display: flex;
    gap: 2.5rem;
    align-items: center;
  }

  nav a {
    color: rgba(255,255,255,0.75);
    text-decoration: none;
    font-size: 0.875rem;
    font-weight: 400;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    transition: color 0.2s;
  }

  nav a:hover { color: #fff; }

  .nav-cta {
    background: rgba(255,255,255,0.12);
    color: #fff !important;
    padding: 0.45rem 1.25rem;
    border-radius: 2px;
    border: 1px solid rgba(255,255,255,0.25);
    transition: background 0.2s !important;
  }

  .nav-cta:hover { background: rgba(255,255,255,0.22) !important; }

  /* ── HERO ── */
  .hero {
    display: grid;
    grid-template-columns: 5fr 7fr;
    min-height: 480px;
    background: #FAF9F6;
  }

  .hero-image {
    background: linear-gradient(135deg, #e8ecf6 0%, #d6dff7 100%);
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .hero-image-inner {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    padding: 3rem;
  }

  .waveform {
    display: flex;
    align-items: center;
    gap: 4px;
    height: 80px;
  }

  .waveform-bar {
    width: 4px;
    background: #1B3280;
    border-radius: 2px;
    opacity: 0.6;
  }

  .phoneme-tag {
    font-family: 'Playfair Display', serif;
    font-size: 3.5rem;
    color: #1B3280;
    opacity: 0.12;
    position: absolute;
    font-style: italic;
  }

  .phoneme-tag:nth-child(1) { top: 15%; left: 10%; font-size: 5rem; }
  .phoneme-tag:nth-child(2) { bottom: 20%; right: 8%; font-size: 4rem; }
  .phoneme-tag:nth-child(3) { top: 50%; left: 40%; font-size: 2.5rem; }

  /* ── HERO CONTENT ── */
  .hero-content {
    padding: 4.5rem 4rem 4.5rem 3rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    border-left: 1px solid #ddd;
  }

  .eyebrow {
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #1B3280;
    font-weight: 500;
    margin-bottom: 1.2rem;
  }

  .hero-content h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 600;
    line-height: 1.15;
    color: #111;
    margin-bottom: 1.5rem;
  }

  .hero-content h1 em {
    font-style: italic;
    color: #1B3280;
  }

  .hero-content p {
    font-size: 1.05rem;
    color: #555;
    line-height: 1.75;
    max-width: 480px;
    margin-bottom: 1rem;
  }

  .hero-content p + p {
    margin-bottom: 0.8rem;
  }

  .engine-note {
    font-size: 0.9rem;
    color: #888;
    font-style: italic;
    margin-bottom: 2rem;
  }

  .engine-note strong {
    color: #333;
    font-style: normal;
  }

  .cta-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: #1B3280;
    color: #fff;
    padding: 0.8rem 2rem;
    font-size: 0.875rem;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    text-decoration: none;
    border-radius: 2px;
    transition: background 0.2s;
    align-self: flex-start;
  }

  .cta-btn:hover { background: #142560; }

  /* ── DIVIDER ── */
  .section-divider {
    height: 2px;
    background: repeating-linear-gradient(
      90deg,
      #1B3280 0px, #1B3280 8px,
      transparent 8px, transparent 16px
    );
    opacity: 0.15;
  }

  /* ── FEATURES ── */
  .features {
    display: grid;
    grid-template-columns: 7fr 5fr;
    min-height: 380px;
    background: #fff;
  }

  .features-content {
    padding: 4rem 3.5rem 4rem 4rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    border-right: 1px solid #ddd;
  }

  .features-content h2 {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 600;
    color: #111;
    margin-bottom: 1.25rem;
    line-height: 1.25;
  }

  .features-content p {
    font-size: 0.975rem;
    color: #555;
    line-height: 1.75;
    margin-bottom: 1rem;
  }

  .feature-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 1.5rem;
  }

  .pill {
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    border: 1px solid #1B3280;
    color: #1B3280;
    padding: 0.35rem 0.9rem;
    border-radius: 2px;
  }

  .features-image {
    background: #F0F3FA;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    position: relative;
    overflow: hidden;
  }

  .feature-grid-illustration {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    width: 200px;
  }

  .feat-card {
    background: #fff;
    border: 1px solid #c8d0e8;
    border-radius: 3px;
    padding: 0.75rem;
    font-size: 0.75rem;
    color: #1B3280;
    font-weight: 500;
    text-align: center;
  }

  .feat-card.accent {
    background: #1B3280;
    color: #fff;
    border-color: #1B3280;
  }

  /* ── LEXICAL TOOLS ── */
  .tools-section {
    padding: 5rem 4rem;
    background: #FAF9F6;
    max-width: 780px;
    margin: 0 auto;
  }

  .tools-section h2 {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 600;
    color: #111;
    margin-bottom: 2.5rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid #1B3280;
    display: inline-block;
  }

  .search-box {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .input-row {
    display: flex;
    gap: 0.75rem;
  }

  .search-box input[type="text"] {
    flex: 1;
    padding: 0.85rem 1.25rem;
    font-size: 1rem;
    font-family: 'DM Sans', sans-serif;
    border: 1.5px solid #d0d0cc;
    background: #fff;
    border-radius: 2px;
    color: #111;
    outline: none;
    transition: border-color 0.2s;
  }

  .search-box input[type="text"]:focus { border-color: #1B3280; }

  .search-box select {
    padding: 0.85rem 2.5rem 0.85rem 1rem;
    font-size: 0.9rem;
    font-family: 'DM Sans', sans-serif;
    border: 1.5px solid #d0d0cc;
    background: #fff;
    border-radius: 2px;
    color: #333;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%231B3280' stroke-width='1.5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 0.9rem center;
    outline: none;
    transition: border-color 0.2s;
    min-width: 140px;
  }

  .search-box select:focus { border-color: #1B3280; }

  #search-btn {
    padding: 0.85rem 2rem;
    background: #1B3280;
    color: #fff;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.875rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    border: none;
    border-radius: 2px;
    cursor: pointer;
    transition: background 0.2s;
  }

  #search-btn:hover { background: #142560; }

  .results-area {
    margin-top: 2rem;
  }

  #results-list {
    list-style: none;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    padding: 0;
  }

  #results-list li {
    background: #fff;
    border: 1px solid #c8d0e8;
    color: #1B3280;
    font-size: 0.9rem;
    padding: 0.4rem 0.9rem;
    border-radius: 2px;
    font-weight: 500;
    letter-spacing: 0.03em;
  }

  .notify {
    color: #888;
    font-size: 0.9rem;
    font-style: italic;
    padding: 0.5rem 0;
  }

  /* ── FOOTER ── */
  .site-footer {
    background: #1B3280;
    padding: 3rem 4rem;
    color: rgba(255,255,255,0.65);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .footer-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    color: rgba(255,255,255,0.9);
    font-style: italic;
  }

  .footer-logo span {
    font-style: normal;
    font-weight: 600;
    color: #a8bfff;
  }

  .footer-links {
    display: flex;
    gap: 2rem;
    font-size: 0.8rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  .footer-links a {
    color: rgba(255,255,255,0.5);
    text-decoration: none;
    transition: color 0.2s;
  }

  .footer-links a:hover { color: rgba(255,255,255,0.9); }

  .footer-copy {
    font-size: 0.78rem;
    color: rgba(255,255,255,0.35);
  }
</style>

<!-- ── HEADER ── -->
<header class="site-header">
  <div class="logo">M<span>-Prosody</span></div>
  <nav>
    <a href="/">Home</a>
    <a href="/lyrical-lab">Lyrical Lab</a>
    <a href="/notebook">Notebook</a>
    <a href="/lyrical-lab" class="nav-cta">Start Writing</a>
  </nav>
</header>

<!-- ── HERO ── -->
<section class="hero">
  <div class="hero-image">
    <span class="phoneme-tag">ə</span>
    <span class="phoneme-tag">ʌ</span>
    <span class="phoneme-tag">ɪ</span>
    <div class="hero-image-inner">
      <div class="waveform">
        {#each [30, 55, 75, 90, 65, 45, 80, 50, 35, 70, 85, 40, 60, 75, 30] as h}
          <div class="waveform-bar" style="height: {h}px;"></div>
        {/each}
      </div>
    </div>
  </div>

  <div class="hero-content">
    <p class="eyebrow">Welcome to M-Prosody</p>
    <h1>Write lyrics that <em>sound</em> right.</h1>
    <p>Experiment with rhymes, synonyms, homophones, and related words. Build your lyrics, check your syllables, and save your creations in your personal notebook.</p>
    <p>M-Prosody's rhyme engine doesn't look at how words are spelled — it listens to how they sound. It matches rhythm, stress, and vowel flow to find rhymes that actually feel right, then ranks them by strength.</p>
    <p class="engine-note">The engine is still evolving. For now, it understands <strong>sound</strong>, not meaning.</p>
    <a href="/lyrical-lab" class="cta-btn">Start Writing →</a>
  </div>
</section>

<div class="section-divider"></div>

<!-- ── FEATURES ── -->
<section class="features">
  <div class="features-content">
    <h2>Everything a lyricist needs.</h2>
    <p>From finding the perfect rhyme to discovering unexpected synonyms — M-Prosody's suite of lexical tools helps you shape language with precision and feel. Each tool is built around how language actually sounds in context.</p>
    <p>Save your favourite words and phrases to your personal notebook, revisit them when inspiration calls, and build a personal lexical library over time.</p>
    <div class="feature-pills">
      <span class="pill">Rhymes</span>
      <span class="pill">Synonyms</span>
      <span class="pill">Homophones</span>
      <span class="pill">Related Words</span>
      <span class="pill">Notebook</span>
    </div>
  </div>

  <div class="features-image">
    <div class="feature-grid-illustration">
      <div class="feat-card accent">Rhyme</div>
      <div class="feat-card">Synonym</div>
      <div class="feat-card">Related</div>
      <div class="feat-card accent">Homophone</div>
    </div>
  </div>
</section>

<div class="section-divider"></div>

<!-- ── LEXICAL TOOLS ── -->
<section id="search">
  <div class="tools-section">
    <h2>Lexical Tools</h2>

    <div class="search-box">
      <div class="input-row">
        <input
          type="text"
          id="word-input"
          placeholder="Enter search here..."
          bind:value={word}
          onkeydown={(e) => e.key === 'Enter' && fetchWordsWrapper()}
        />
        <select id="search-type" bind:value={selected}>
          <option value="rhyme">Rhyme</option>
          <option value="synonym">Synonym</option>
          <option value="related">Related</option>
          <option value="homophone">Homophone</option>
        </select>
        <button id="search-btn" onclick={fetchWordsWrapper}>Find Words</button>
      </div>
    </div>

    <div class="results-area">
      {#if isLoading}
        <SigilSpinner text="Consulting the lexicon…" />
      {:else}
        {#if wordList.length > 0 || phraseList.length > 0}
          <ul id="results-list">
            {#if phraseList.length > 0}
              {#each phraseList as lst (lst.phrase)}
                <li>{lst.phrase}</li>
              {/each}
            {/if}
            {#each wordList as lst (lst.word)}
              <li>{lst.word}</li>
            {/each}
          </ul>
        {:else}
          <div class="notify">
            <p>{notify}</p>
          </div>
        {/if}
      {/if}
    </div>
  </div>
</section>

<!-- ── FOOTER ── -->
<footer class="site-footer">
  <div class="footer-logo">M<span>-Prosody</span></div>
  <div class="footer-links">
    <a href="/">Home</a>
    <a href="/lyrical-lab">Lab</a>
    <a href="/notebook">Notebook</a>
  </div>
  <div class="footer-copy">© 2025 M-Prosody</div>
</footer>