<script lang="ts">
	const downloads = [
		{
			name: 'Windows',
			icon: '/icons8-windows-11-64.png',
			version: 'v1.0.0',
			size: '145 MB',
			link: '#',
            disabled: true
		},
		{
			name: 'Linux',
			icon: '/icons8-linux-64.png',
			version: 'v1.0.0',
			size: '138 MB',
			link: '#',
            disabled: true
		},
		{
			name: 'macOS',
			icon: '/icons8-apple-inc-64.png',
			version: 'Coming Soon',
			size: '--',
			link: '#',
			disabled: true
		}
	];
</script>

<svelte:head>
	<title>M-Prosody — Download</title>
	<meta
		name="description"
		content="Download M-Prosody — a lyric writing environment designed for artists, storytellers, and dreamers."
	/>
</svelte:head>

<div class="text-column">
	<section class="hero">
		<p class="hero-text">
			Words are rhythm. Rhythm becomes emotion. Emotion becomes memory.
		</p>

		<h1>M-Prosody Desktop</h1>

		<p class="hero-tagline">
			A lyric writing environment built for poets, rappers, storytellers, and restless minds.
		</p>
	</section>

	<section>
		<h2>Download M-Prosody</h2>

		<p>
			M-Prosody is designed to make writing feel immersive rather than mechanical.
			Whether you're crafting verses at 2AM or shaping fragments into meaning,
			the desktop experience keeps your creativity close and distraction far away.
		</p>

		<div class="download-grid">
			{#each downloads as app}
				<div class:disabled={app.disabled} class="download-card">
					<div class="card-top">
						<div class="platform">
							<span class="icon">
                                <img src={app.icon} alt="distro icon">
                            </span>
							<div>
								<h3>{app.name}</h3>
								<p>{app.version}</p>
							</div>
						</div>

						<span class="size">{app.size}</span>
					</div>

					<a
						href={app.link}
						class="download-btn"
						class:inactive={app.disabled}
					>
						{app.disabled ? 'Coming Soon' : 'Download'}
					</a>
				</div>
			{/each}
		</div>
	</section>

	<section>
		<h2>What You Get</h2>

		<ul>
			<li>Focused lyric writing workspace</li>
			<li>Rhyme and creative assistance tools</li>
			<li>Minimal, atmospheric interface</li>
			<li>Offline desktop experience</li>
			<li>Built for deep writing sessions</li>
		</ul>

		<blockquote>
			“M-Prosody doesn't try to write for you.  
			It tries to pull more out of you.”
		</blockquote>
	</section>

	<section>
		<h2>System Requirements</h2>

		<ul>
			<li>Windows 10/11 or modern Linux distribution</li>
			<li>4 GB RAM minimum</li>
			<li>200 MB available storage</li>
			<li>Internet connection required for some AI features</li>
		</ul>
	</section>

	<div class="final-note">
		<p>Built for creators who treat words like architecture.</p>
		<p>Welcome to the laboratory of rhythm </p>
	</div>
</div>

<style>
	:global(body) {
		margin: 0;
		background:
			radial-gradient(circle at top, rgba(140, 82, 255, 0.12), transparent 40%),
			#0b0613;
		font-family: 'Inter', sans-serif;
		color: #f3e8ff;
	}

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

	h1 {
		font-size: clamp(2.5rem, 5vw, 4rem);
		line-height: 1.1;
		margin: 0;
		color: #f3d8ff;
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
		border-radius: 6px;
	}

	.download-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
		gap: 1rem;
		margin-top: 2rem;
	}

	.download-card {
		background: rgba(199, 125, 255, 0.06);
		border: 1px solid rgba(200, 120, 255, 0.2);
		border-radius: 16px;
		padding: 1.2rem;
		backdrop-filter: blur(10px);
		transition:
			transform 0.2s ease,
			border-color 0.2s ease,
			background 0.2s ease;
	}

	.download-card:hover {
		transform: translateY(-4px);
		border-color: rgba(224, 170, 255, 0.5);
		background: rgba(199, 125, 255, 0.1);
	}

	.disabled {
		opacity: 0.6;
	}

	.card-top {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 1.5rem;
	}

	.platform {
		display: flex;
		align-items: center;
		gap: 0.8rem;
	}

	.platform h3 {
		margin: 0;
		color: #f0d3ff;
		font-size: 1.1rem;
	}

	.platform p {
		margin: 0;
		font-size: 0.9rem;
		color: #cfa7ff;
	}

	.icon {
		font-size: 2rem;
	}

	.size {
		font-size: 0.85rem;
		color: #b98adf;
	}

	.download-btn {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		padding: 0.85rem 1rem;
		border-radius: 10px;
		text-decoration: none;
		font-weight: 600;
		background: linear-gradient(135deg, #c77dff, #9d4edd);
		color: white;
		transition:
			transform 0.2s ease,
			opacity 0.2s ease;
	}

	.download-btn:hover {
		transform: scale(1.02);
	}

	.inactive {
		pointer-events: none;
		background: rgba(255, 255, 255, 0.08);
		color: #cba5e6;
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

	@media (max-width: 640px) {
		.card-top {
			flex-direction: column;
			align-items: flex-start;
			gap: 0.8rem;
		}
	}
</style>
