<script>
  import { apiPost } from "$lib/api/api_proxy";
	let exampleWord = $state('time');
	let response = $state(null);
	let loading = $state(false);
    import {get_url} from "$lib/url_vars/urls_vars"

	async function tryExample() {
		loading = true;
		response = null;

		try {
      response = await apiPost(`/api/public/get-rhymes`, { word: exampleWord })
		} catch (err) {
			response = { error: 'Request failed' };
		} finally {
			loading = false;
		}
	}

	const curlExample = `curl -X POST ${get_url()}/api/public/get-rhymes \\
  -H "Content-Type: application/json" \\
  -d '{"word": "time"}'`;

	const jsExample = `fetch('${get_url}/api/public/get-rhymes', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ word: 'time' })
})
.then(res => res.json())
.then(data => console.log(data));`;
</script>

<div class="api-container">
	<h1>Public Rhyme API</h1>
	<p class="tagline">Turn words into echoes. Find what resonates.</p>


	<section class="rhyme-engine">
	<h2>How the rhyme engine works</h2>

		<p>
			Most rhyme tools look at how words are <strong>spelled</strong>.
			<br />
			M-Prosody listens to how words <strong>sound</strong>.
		</p>

		<p>
			When you enter a word, the engine breaks it down into:
		</p>

		<ul>
			<li>how many beats it has</li>
			<li>where the stress falls</li>
			<li>how the vowel sounds flow</li>
		</ul>

		<p>
			Then it searches for words and phrases that <strong>match that pattern</strong>—
			especially toward the <em>end</em>, where rhymes naturally live.
		</p>

		<p>
			That’s why it can find:
		</p>

		<ul>
			<li><strong>multi-syllable rhymes</strong></li>
			<li><strong>near (slant) rhymes</strong></li>
			<li>and even rhymes for <strong>unusual or invented words</strong></li>
		</ul>

		<p>
			Instead of giving you random matches, it <strong>ranks results by how strong the rhyme feels</strong>—
			so the best ones rise to the top.
		</p>

		<p class="closing">
			It doesn’t just match words.<br />
			It follows the rhythm behind them.
		</p>
	</section>

	<section>
		<h2>Endpoint</h2>
		<code>/api/public/get-rhymes</code>
	</section>

	<section>
		<h2>Request</h2>
		<p>Send a POST request with JSON:</p>
		<pre>{`{ "word": "example" }`}</pre>
	</section>

	<section>
		<h2>Response</h2>
		<pre>{`{
  "word_rhymes": [...],
  "phrasal_rhymes": [...],
  "total_word_rhymes": 0,
  "total_phrasal_rhymes": 0
}`}</pre>
	</section>

	<section>
		<h2>Try it</h2>
		<input bind:value={exampleWord} placeholder="Enter a word..." />
		<button onclick={tryExample} disabled={loading}>
			{loading ? 'Searching…' : 'Find Rhymes'}
		</button>

		{#if response}
			<pre class="response">{JSON.stringify(response, null, 2)}</pre>
		{/if}
	</section>

	<section>
		<h2>Examples</h2>

		<h3>cURL</h3>
		<pre>{curlExample}</pre>

		<h3>JavaScript</h3>
		<pre>{jsExample}</pre>
	</section>

	
</div>

<style>
	.api-container {
		max-width: 700px;
		margin: 2rem auto;
		padding: 1.5rem;
		background: linear-gradient(145deg, #140824, #1f0d36);
		border-radius: 14px;
		box-shadow:
			0 0 12px rgba(128, 0, 255, 0.25),
			inset 0 0 10px rgba(128, 0, 255, 0.1);
		color: #e2c6ff;
		font-family: 'Fira Mono', monospace;
	}

	h1 {
		margin-bottom: 0.3rem;
	}

	.tagline {
		opacity: 0.8;
		margin-bottom: 1.5rem;
		font-style: italic;
	}

	section {
		margin-bottom: 1.5rem;
	}

	code {
		background: #1a0a2b;
		padding: 0.3rem 0.5rem;
		border-radius: 6px;
	}

	pre {
		background: #1a0a2b;
		padding: 0.8rem;
		border-radius: 10px;
		overflow-x: auto;
		border: 1px solid rgba(128, 0, 255, 0.2);
	}

	input {
		width: 100%;
		padding: 0.6rem;
		margin-bottom: 0.8rem;
		border-radius: 8px;
		border: 1px solid rgba(128, 0, 255, 0.2);
		background: #1a0a2b;
		color: #e2c6ff;
	}

	button {
		padding: 0.6rem 1rem;
		border-radius: 8px;
		border: none;
		background: linear-gradient(135deg, #7c3aed, #a855f7);
		color: white;
		cursor: pointer;
	}

	.response {
		margin-top: 1rem;
		max-height: 300px;
		overflow-y: auto;
		overflow-x: hidden;

		padding: 0.8rem;
		border-radius: 10px;
		background: #1a0a2b;
		border: 1px solid rgba(128, 0, 255, 0.2);

		/* Firefox */
		scrollbar-width: thin;
		scrollbar-color: #a855f7 transparent;
		}

	.response::-webkit-scrollbar {
		width: 8px;
	}

	.response::-webkit-scrollbar-track {
		background: transparent;
	}

	.response::-webkit-scrollbar-thumb {
		background: linear-gradient(180deg, #7c3aed, #a855f7);
		border-radius: 10px;
		box-shadow: 0 0 6px rgba(168, 85, 247, 0.5);
	}

	.response::-webkit-scrollbar-thumb:hover {
		background: linear-gradient(180deg, #9333ea, #c084fc);
	}


	.rhyme-engine {
		max-width: 650px;
		margin: 3rem auto;
		padding: 1.5rem;
		background: linear-gradient(145deg, #140824, #1f0d36);
		border-radius: 14px;
		box-shadow:
			0 0 12px rgba(128, 0, 255, 0.25),
			inset 0 0 10px rgba(128, 0, 255, 0.1);
		color: #e2c6ff;
		font-family: 'Fira Mono', monospace;
	}

	.rhyme-engine h2 {
		margin-bottom: 1rem;
		color: #d8b3ff;
	}

	.rhyme-engine p {
		margin-bottom: 1rem;
		line-height: 1.5;
	}

	.rhyme-engine ul {
		margin: 0.5rem 0 1rem 1.2rem;
	}

	.rhyme-engine li {
		margin-bottom: 0.3rem;
	}

	.rhyme-engine .closing {
		margin-top: 1.5rem;
		font-style: italic;
		text-align: center;
		color: #c084fc;
	}



	/* =========================================
   MEDIA QUERIES — Public Rhyme API Page
   xs: < 375px  |  sm: 375–639px  |  md: 640–1023px
   lg: 1024–1279px  |  xl: 1280+  |  2xl: 1600+
   ========================================= */

/* -----------------------------------------
   XS — Very small phones (< 375px)
   ----------------------------------------- */
@media (max-width: 374px) {
  .api-container {
    max-width: 100%;
    margin: 0.75rem 0.5rem;
    padding: 1rem 0.875rem;
    border-radius: 10px;
  }

  h1 {
    font-size: 1.25rem;
    margin-bottom: 0.25rem;
  }

  .tagline {
    font-size: 0.8rem;
    margin-bottom: 1rem;
  }

  section {
    margin-bottom: 1.1rem;
  }

  /* h2 inside sections */
  section h2 {
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
  }

  section h3 {
    font-size: 0.85rem;
    margin-bottom: 0.4rem;
  }

  section p {
    font-size: 0.82rem;
    line-height: 1.55;
  }

  section ul {
    margin: 0.5rem 0 0.75rem 1rem;
  }

  section li {
    font-size: 0.82rem;
    margin-bottom: 0.3rem;
  }

  code {
    font-size: 0.78rem;
    padding: 0.25rem 0.4rem;
    /* Allow wrapping on very narrow screens */
    word-break: break-all;
  }

  pre {
    padding: 0.6rem 0.75rem;
    font-size: 0.72rem;
    border-radius: 8px;
    /* Horizontal scroll is intentional for code blocks */
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  input {
    font-size: 0.82rem;
    padding: 0.5rem 0.6rem;
    border-radius: 6px;
    margin-bottom: 0.6rem;
  }

  button {
    width: 100%;              /* Full-width tap target on xs */
    padding: 0.6rem 0.875rem;
    font-size: 0.82rem;
    border-radius: 6px;
  }

  .response {
    max-height: 220px;
    font-size: 0.72rem;
    padding: 0.6rem;
    border-radius: 8px;
    margin-top: 0.75rem;
  }

  .response::-webkit-scrollbar {
    width: 4px;
  }

  /* Rhyme engine card */
  .rhyme-engine {
    max-width: 100%;
    margin: 1.5rem 0;
    padding: 1rem 0.875rem;
    border-radius: 10px;
  }

  .rhyme-engine h2 {
    font-size: 0.95rem;
    margin-bottom: 0.75rem;
  }

  .rhyme-engine p {
    font-size: 0.82rem;
    margin-bottom: 0.75rem;
    line-height: 1.55;
  }

  .rhyme-engine ul {
    margin: 0.4rem 0 0.75rem 1rem;
  }

  .rhyme-engine li {
    font-size: 0.82rem;
    margin-bottom: 0.25rem;
  }

  .rhyme-engine .closing {
    font-size: 0.82rem;
    margin-top: 1rem;
  }
}

/* -----------------------------------------
   SM — Standard phones (375px – 639px)
   ----------------------------------------- */
@media (min-width: 375px) and (max-width: 639px) {
  .api-container {
    max-width: 100%;
    margin: 1rem 0.75rem;
    padding: 1.1rem 1rem;
    border-radius: 11px;
  }

  h1 {
    font-size: 1.4rem;
  }

  .tagline {
    font-size: 0.85rem;
    margin-bottom: 1.1rem;
  }

  section {
    margin-bottom: 1.25rem;
  }

  section h2 {
    font-size: 1rem;
  }

  section h3 {
    font-size: 0.9rem;
  }

  section p,
  section li {
    font-size: 0.85rem;
    line-height: 1.6;
  }

  code {
    font-size: 0.82rem;
    word-break: break-all;
  }

  pre {
    font-size: 0.76rem;
    padding: 0.65rem 0.8rem;
    border-radius: 8px;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  input {
    font-size: 0.85rem;
    padding: 0.55rem 0.65rem;
  }

  button {
    width: 100%;
    font-size: 0.85rem;
    padding: 0.65rem 1rem;
  }

  .response {
    max-height: 240px;
    font-size: 0.76rem;
    padding: 0.65rem;
  }

  .response::-webkit-scrollbar {
    width: 5px;
  }

  .rhyme-engine {
    max-width: 100%;
    margin: 1.75rem 0;
    padding: 1.1rem 1rem;
    border-radius: 11px;
  }

  .rhyme-engine h2 {
    font-size: 1rem;
  }

  .rhyme-engine p,
  .rhyme-engine li {
    font-size: 0.85rem;
    line-height: 1.6;
  }

  .rhyme-engine .closing {
    font-size: 0.85rem;
    margin-top: 1.1rem;
  }
}

/* -----------------------------------------
   MD — Large phones / small tablets (640px – 1023px)
   ----------------------------------------- */
@media (min-width: 640px) and (max-width: 1023px) {
  .api-container {
    max-width: 92%;
    margin: 1.5rem auto;
    padding: 1.25rem 1.1rem;
    border-radius: 12px;
  }

  h1 {
    font-size: 1.6rem;
  }

  .tagline {
    font-size: 0.9rem;
  }

  section h2 {
    font-size: 1.1rem;
  }

  section h3 {
    font-size: 0.95rem;
  }

  section p,
  section li {
    font-size: 0.88rem;
    line-height: 1.6;
  }

  code {
    font-size: 0.85rem;
  }

  pre {
    font-size: 0.8rem;
    padding: 0.7rem 0.875rem;
  }

  input {
    font-size: 0.88rem;
  }

  button {
    font-size: 0.88rem;
    padding: 0.65rem 1.1rem;
  }

  .response {
    max-height: 260px;
    font-size: 0.8rem;
  }

  .rhyme-engine {
    max-width: 100%;
    margin: 2rem auto;
    padding: 1.25rem 1.1rem;
  }

  .rhyme-engine h2 {
    font-size: 1.1rem;
  }

  .rhyme-engine p,
  .rhyme-engine li {
    font-size: 0.88rem;
  }

  .rhyme-engine .closing {
    font-size: 0.88rem;
  }
}

/* -----------------------------------------
   LG — Tablets / small laptops (1024px – 1279px)
   ----------------------------------------- */
@media (min-width: 1024px) and (max-width: 1279px) {
  .api-container {
    max-width: 660px;
    margin: 1.75rem auto;
    padding: 1.4rem;
  }

  h1 {
    font-size: 1.75rem;
  }

  section h2 {
    font-size: 1.15rem;
  }

  pre {
    font-size: 0.83rem;
  }

  .response {
    max-height: 280px;
    font-size: 0.83rem;
  }

  .rhyme-engine {
    max-width: 620px;
    margin: 2.5rem auto;
    padding: 1.4rem;
  }

  .rhyme-engine h2 {
    font-size: 1.15rem;
  }
}

/* -----------------------------------------
   XL — Standard desktops (1280px – 1599px)
   ----------------------------------------- */
@media (min-width: 1280px) {
  /* Base styles are tuned for this range — preserved.
     api-container max-width: 700px,
     rhyme-engine max-width: 650px,
     padding: 1.5rem are all intentional. */

  button {
    /* Restore auto width — full-width only needed on mobile */
    width: auto;
  }
}

/* -----------------------------------------
   2XL — Large / wide monitors (1600px+)
   ----------------------------------------- */
@media (min-width: 1600px) {
  .api-container {
    max-width: 800px;
    margin: 2.5rem auto;
    padding: 2rem;
    border-radius: 16px;
  }

  h1 {
    font-size: 2.1rem;
    margin-bottom: 0.4rem;
  }

  .tagline {
    font-size: 1rem;
    margin-bottom: 1.75rem;
  }

  section {
    margin-bottom: 1.875rem;
  }

  section h2 {
    font-size: 1.35rem;
    margin-bottom: 0.75rem;
  }

  section h3 {
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
  }

  section p,
  section li {
    font-size: 1rem;
    line-height: 1.65;
  }

  code {
    font-size: 0.95rem;
    padding: 0.35rem 0.6rem;
  }

  pre {
    font-size: 0.9rem;
    padding: 1rem 1.1rem;
    border-radius: 12px;
  }

  input {
    font-size: 0.95rem;
    padding: 0.75rem 0.875rem;
    border-radius: 10px;
    margin-bottom: 0.9rem;
  }

  button {
    padding: 0.75rem 1.25rem;
    font-size: 0.95rem;
    border-radius: 10px;
  }

  .response {
    max-height: 340px;
    font-size: 0.9rem;
    padding: 1rem;
    border-radius: 12px;
    margin-top: 1.1rem;
  }

  .response::-webkit-scrollbar {
    width: 10px;
  }

  .rhyme-engine {
    max-width: 750px;
    margin: 3.5rem auto;
    padding: 2rem;
    border-radius: 16px;
  }

  .rhyme-engine h2 {
    font-size: 1.35rem;
    margin-bottom: 1.1rem;
  }

  .rhyme-engine p {
    font-size: 1rem;
    margin-bottom: 1.1rem;
    line-height: 1.65;
  }

  .rhyme-engine li {
    font-size: 1rem;
    margin-bottom: 0.4rem;
  }

  .rhyme-engine .closing {
    font-size: 1rem;
    margin-top: 1.75rem;
  }
}
</style>
