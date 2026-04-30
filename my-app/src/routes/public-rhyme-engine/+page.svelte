<script>
	let exampleWord = $state('time');
	let response = $state(null);
	let loading = $state(false);
    import {get_url} from "$lib/url_vars/urls_vars"

	async function tryExample() {
		loading = true;
		response = null;

		try {
			const res = await fetch(`${get_url()}/api/public/get-rhymes`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ word: exampleWord })
			});

			response = await res.json();
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
</style>
