<script lang="ts">
	import { resolve } from '$app/paths';
</script>

<svelte:head>
	<title>About M-Prosody</title>
	<meta name="description" content="About M-Prosody - A lyric writing app for songwriters" />
</svelte:head>

<div class="text-column">
	<div class="hero">
		<p class="hero-text">Somewhere between silence and sound, there's a fragile moment where a lyric is born.</p>
		<p class="hero-text">A rhythm searching for words. A thought trying to become music.</p>
		<p class="hero-tagline"><strong>M-Prosody</strong> was built for that moment.</p>
	</div>

	<section>
		<h2>What it is</h2>
		<p>
			M-Prosody is a <strong>free web and desktop lyric writing app</strong> designed to give lyricists a focused, intelligent space to create.
		</p>
		<p>
			It brings together the essential tools of songwriting into one environment—so you can stay in your flow instead of jumping between tabs, apps, and distractions.
		</p>
		<p>Whether you're writing your first verse or refining your tenth version, M-Prosody is built to move with you.</p>
	</section>

	<section>
		<h2>Why it exists</h2>
		<p>Most writing tools weren't made for lyricists.</p>
		<p>They don't understand:</p>
		<ul>
			<li>rhythm</li>
			<li>flow</li>
			<li>rhyme complexity</li>
			<li>or the way a single word can change everything</li>
		</ul>
		<p>So writers adapt. They open multiple tabs. They break their concentration. They lose the very thing they're trying to capture.</p>
		<p>M-Prosody exists to fix that.</p>
		<blockquote>One space. One process. One uninterrupted creative flow.</blockquote>
	</section>

	<section>
		<h2>What it offers</h2>
		<p>M-Prosody gives you a complete lyric writing environment with tools that support both creativity and precision:</p>
		<ul>
			<li><strong>Focused lyric workspace</strong> for distraction-free writing</li>
			<li><strong>Flow checker</strong> to refine rhythm and delivery</li>
			<li><strong>Multi-syllable rhyme dictionary</strong> <em>(available offline on desktop)</em></li>
			<li><strong>Figure of speech generator</strong> <em>(offline on desktop)</em></li>
			<li><strong>Word tools</strong> including homophones, synonyms, and related words</li>
			<li><strong>AI lyric generation</strong> based on genre</li>
			<li><strong>Song versioning</strong> to track your creative evolution</li>
			<li><strong>Cloud syncing</strong> between desktop and web</li>
			<li><strong>Offline-first desktop experience</strong> so you can write anywhere</li>
		</ul>
	</section>

	<section>
		<h2>Built for how you write</h2>
		<p>M-Prosody is designed with a simple idea:</p>
		<blockquote>Writing comes first. Everything else supports it.</blockquote>
		<p>
			The desktop app works offline so you can create without interruption.
			When you're ready, you can sync your work and continue anywhere.
		</p>
		<p>No forced connectivity. No unnecessary friction.</p>
		<p>Just you and your craft.</p>
	</section>

	<section>
		<h2>Who it's for</h2>
		<p>M-Prosody is for:</p>
		<ul>
			<li>lyricists</li>
			<li>songwriters</li>
			<li>rappers</li>
			<li>poets</li>
			<li>and anyone who treats words like instruments</li>
		</ul>
		<p>Especially those who value:</p>
		<ul>
			<li>focus</li>
			<li>privacy</li>
			<li>control</li>
			<li>and creative depth</li>
		</ul>
	</section>

	<section>
		<h2>What makes it different</h2>
		<p>M-Prosody isn't just a tool—it's a writing environment.</p>
		<p>It doesn't try to replace your creativity. It strengthens it.</p>
		<p>It doesn't overwhelm you with features. It gives you exactly what you need, when you need it.</p>
	</section>

	<section>
		<h2>Looking forward</h2>
		<p>M-Prosody is just getting started.</p>
		<p>
			New features, deeper tools, and expanded capabilities are on the way—while keeping the core experience simple, focused, and accessible.
		</p>
		<p>Everything available today is free, with more to come.</p>
	</section>

	<section class="final-note">
		<p>Words carry weight. Rhythm gives them life.</p>
		<p><strong>M-Prosody exists to help you shape both.</strong></p>
	</section>
</div>

<style>
	.text-column {
		max-width: 800px;
		margin: 0 auto;
		padding: 2rem 1rem;
		line-height: 1.8;
		color: #e6ccff;
	}

	.hero {
		margin-bottom: 3rem;
		padding-bottom: 2rem;
		border-bottom: 1px solid rgba(200, 120, 255, 0.2);
	}

	.hero-text {
		font-size: 1.1rem;
		margin-bottom: 1rem;
		font-style: italic;
		color: #d4a5ff;
	}

	.hero-tagline {
		font-size: 1.2rem;
		margin-top: 1.5rem;
		color: #c77dff;
	}

	h2 {
		font-size: 1.8rem;
		margin-top: 2rem;
		margin-bottom: 1rem;
		color: #e0aaff;
		border-left: 3px solid #c77dff;
		padding-left: 1rem;
	}

	section {
		margin-bottom: 2.5rem;
	}

	p {
		margin-bottom: 1rem;
	}

	ul {
		margin: 1rem 0 1rem 1.5rem;
		padding: 0;
	}

	li {
		margin-bottom: 0.5rem;
		color: #d4a5ff;
	}

	blockquote {
		margin: 1.5rem 0;
		padding: 1rem 1.5rem;
		border-left: 3px solid #c77dff;
		background: rgba(199, 125, 255, 0.05);
		font-style: italic;
		color: #d4a5ff;
		font-size: 1.05rem;
	}

	.final-note {
		background: rgba(199, 125, 255, 0.08);
		padding: 2rem;
		border-radius: 8px;
		border: 1px solid rgba(200, 120, 255, 0.2);
		text-align: center;
		font-size: 1.1rem;
		margin-top: 3rem;
	}

	.final-note p {
		margin-bottom: 0.5rem;
	}

	a {
		color: #c77dff;
		text-decoration: none;
		border-bottom: 1px solid #c77dff;
		transition: all 0.3s ease;
	}

	a:hover {
		color: #e0aaff;
		border-bottom-color: #e0aaff;
	}


	/* =========================================
   MEDIA QUERIES — About / Landing Page
   xs: < 375px  |  sm: 375–639px  |  md: 640–1023px
   lg: 1024–1279px  |  xl: 1280+  |  2xl: 1600+
   ========================================= */

/* -----------------------------------------
   XS — Very small phones (< 375px)
   ----------------------------------------- */
@media (max-width: 374px) {
  .text-column {
    width: 100%;
    padding: 1.25rem 0.875rem;
    line-height: 1.7;
  }

  .hero {
    margin-bottom: 1.75rem;
    padding-bottom: 1.25rem;
  }

  .hero-text {
    font-size: 0.92rem;
    margin-bottom: 0.75rem;
  }

  .hero-tagline {
    font-size: 1rem;
    margin-top: 1rem;
  }

  h2 {
    font-size: 1.25rem;
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
    padding-left: 0.75rem;
    /* Thinner accent bar — 3px is proportionally heavy on xs */
    border-left-width: 2px;
  }

  section {
    margin-bottom: 1.75rem;
  }

  p {
    font-size: 0.88rem;
    margin-bottom: 0.75rem;
  }

  ul {
    margin: 0.75rem 0 0.75rem 1.1rem;
  }

  li {
    font-size: 0.88rem;
    margin-bottom: 0.4rem;
  }

  blockquote {
    margin: 1rem 0;
    padding: 0.75rem 1rem;
    font-size: 0.92rem;
    border-left-width: 2px;
  }

  .final-note {
    padding: 1.25rem;
    border-radius: 6px;
    font-size: 0.92rem;
    margin-top: 2rem;
  }
}

/* -----------------------------------------
   SM — Standard phones (375px – 639px)
   ----------------------------------------- */
@media (min-width: 375px) and (max-width: 639px) {
  .text-column {
    max-width: 100%;
    padding: 1.5rem 1rem;
    line-height: 1.75;
  }

  .hero {
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
  }

  .hero-text {
    font-size: 0.975rem;
    margin-bottom: 0.875rem;
  }

  .hero-tagline {
    font-size: 1.05rem;
    margin-top: 1.25rem;
  }

  h2 {
    font-size: 1.35rem;
    margin-top: 1.75rem;
    margin-bottom: 0.875rem;
    padding-left: 0.875rem;
  }

  section {
    margin-bottom: 2rem;
  }

  p {
    font-size: 0.9rem;
    margin-bottom: 0.875rem;
  }

  ul {
    margin: 0.875rem 0 0.875rem 1.25rem;
  }

  li {
    font-size: 0.9rem;
    margin-bottom: 0.45rem;
  }

  blockquote {
    margin: 1.25rem 0;
    padding: 0.875rem 1.1rem;
    font-size: 0.95rem;
  }

  .final-note {
    padding: 1.5rem;
    font-size: 0.975rem;
    margin-top: 2.25rem;
    border-radius: 7px;
  }
}

/* -----------------------------------------
   MD — Large phones / small tablets (640px – 1023px)
   ----------------------------------------- */
@media (min-width: 640px) and (max-width: 1023px) {
  .text-column {
    max-width: 680px;
    padding: 1.75rem 1.25rem;
  }

  .hero {
    margin-bottom: 2.25rem;
    padding-bottom: 1.75rem;
  }

  .hero-text {
    font-size: 1rem;
  }

  .hero-tagline {
    font-size: 1.1rem;
  }

  h2 {
    font-size: 1.5rem;
    margin-top: 1.875rem;
  }

  section {
    margin-bottom: 2.25rem;
  }

  p {
    font-size: 0.95rem;
  }

  li {
    font-size: 0.95rem;
  }

  blockquote {
    font-size: 1rem;
    padding: 0.9rem 1.25rem;
  }

  .final-note {
    padding: 1.75rem;
    font-size: 1rem;
    margin-top: 2.5rem;
  }
}

/* -----------------------------------------
   LG — Tablets / small laptops (1024px – 1279px)
   ----------------------------------------- */
@media (min-width: 1024px) and (max-width: 1279px) {
  .text-column {
    max-width: 740px;
    padding: 1.875rem 1rem;
  }

  .hero {
    margin-bottom: 2.5rem;
    padding-bottom: 1.875rem;
  }

  .hero-text {
    font-size: 1.05rem;
  }

  .hero-tagline {
    font-size: 1.15rem;
  }

  h2 {
    font-size: 1.65rem;
    margin-top: 1.875rem;
  }

  section {
    margin-bottom: 2.375rem;
  }

  blockquote {
    font-size: 1.02rem;
  }

  .final-note {
    padding: 1.875rem;
    font-size: 1.05rem;
    margin-top: 2.75rem;
  }
}

/* -----------------------------------------
   XL — Standard desktops (1280px – 1599px)
   ----------------------------------------- */
@media (min-width: 1280px) {
  /* Base styles are tuned for this range — preserved.
     max-width: 800px, padding: 2rem 1rem,
     h2: 1.8rem, hero-text: 1.1rem are all intentional. */

  .text-column {
    max-width: 800px;         /* Matches base */
    padding: 2rem 1rem;
  }
}

/* -----------------------------------------
   2XL — Large / wide monitors (1600px+)
   ----------------------------------------- */
@media (min-width: 1600px) {
  .text-column {
    max-width: 900px;         /* Wider column — more breathing room */
    padding: 2.5rem 1rem;
    line-height: 1.9;
  }

  .hero {
    margin-bottom: 3.5rem;
    padding-bottom: 2.5rem;
  }

  .hero-text {
    font-size: 1.2rem;
    margin-bottom: 1.1rem;
  }

  .hero-tagline {
    font-size: 1.35rem;
    margin-top: 1.75rem;
  }

  h2 {
    font-size: 2rem;
    margin-top: 2.25rem;
    margin-bottom: 1.1rem;
    padding-left: 1.25rem;
  }

  section {
    margin-bottom: 3rem;
  }

  p {
    font-size: 1.05rem;
    margin-bottom: 1.1rem;
  }

  ul {
    margin: 1.1rem 0 1.1rem 1.75rem;
  }

  li {
    font-size: 1.05rem;
    margin-bottom: 0.6rem;
  }

  blockquote {
    margin: 1.75rem 0;
    padding: 1.25rem 1.75rem;
    font-size: 1.15rem;
  }

  .final-note {
    padding: 2.5rem;
    border-radius: 10px;
    font-size: 1.2rem;
    margin-top: 3.5rem;
  }
}
</style>
