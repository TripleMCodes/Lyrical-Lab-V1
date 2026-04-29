<script>

	import {get_url} from "$lib/url_vars/urls_vars"
	let email = $state('');
	let subject = $state('');
	let message = $state('');
	let isSending = $state(false);
	let status = $state('');

	async function handleSubmit() {
		isSending = true;
		status = '';

		try {

			const res = await fetch(`${get_url()}/api/contact`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ "email":email, "subject":subject, "message":message })
			});

			if (!res.ok) throw new Error('Failed to send message');

			status = 'Message received. Thank you.';
			email = '';
			subject = '';
			message = '';
		} catch (err) {
			console.error(err);
			status = 'Something went wrong. Please try again.';
		} finally {
			isSending = false;
		}
	}
</script>

<div class="contact-container">
	<h1>Contact Us</h1>
	<p class="subtitle">
		Somewhere between questions and answers, there’s a conversation worth having.
	</p>

	<p class="intro">
		If something isn’t working, if you have an idea, or if you just want to reach out—this space is yours.
		M-Prosody is still evolving, and every message shapes it.
	</p>

	<form on:submit|preventDefault={handleSubmit}>
		<label>
			Email Address
			<input type="email" bind:value={email} placeholder="you@example.com" required />
		</label>

		<label>
			Subject
			<input type="text" bind:value={subject} placeholder="What’s this about?" required />
		</label>

		<label>
			Message
			<textarea bind:value={message} placeholder="Write freely…" rows="6" required></textarea>
		</label>

		<button type="submit" disabled={isSending}>
			{isSending ? 'Sending…' : 'Send Message'}
		</button>

		{#if status}
			<p class="status">{status}</p>
		{/if}
	</form>
</div>

<style>
	.contact-container {
		max-width: 560px;
		margin: 3rem auto;
		padding: 1.8rem;
		border-radius: 14px;
		background: linear-gradient(145deg, #140824, #1f0d36);
		box-shadow:
			0 0 14px rgba(128, 0, 255, 0.25),
			inset 0 0 10px rgba(128, 0, 255, 0.12);
		color: #e2c6ff;
		font-family: 'Fira Mono', monospace;
	}

	h1 {
		margin-bottom: 0.5rem;
		color: #d8b3ff;
	}

	.subtitle {
		opacity: 0.85;
		margin-bottom: 1rem;
		font-style: italic;
	}

	.intro {
		font-size: 0.95rem;
		margin-bottom: 1.5rem;
		line-height: 1.4;
	}

	label {
		display: block;
		margin-bottom: 1rem;
		font-size: 0.9rem;
	}

	input,
	textarea {
		width: 100%;
		margin-top: 0.4rem;
		padding: 0.65rem;
		border-radius: 8px;
		border: 1px solid rgba(128, 0, 255, 0.25);
		background: #1a0a2b;
		color: #e2c6ff;
		outline: none;
		transition: 0.2s ease;
	}

	input:focus,
	textarea:focus {
		border-color: #a855f7;
		box-shadow: 0 0 8px rgba(168, 85, 247, 0.4);
	}

	button {
		width: 100%;
		padding: 0.75rem;
		border: none;
		border-radius: 10px;
		background: linear-gradient(135deg, #7c3aed, #a855f7);
		color: white;
		cursor: pointer;
		transition: 0.2s ease;
		font-weight: 600;
	}

	button:hover {
		transform: translateY(-2px);
		box-shadow: 0 0 12px rgba(168, 85, 247, 0.5);
	}

	button:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.status {
		margin-top: 1rem;
		font-size: 0.9rem;
		opacity: 0.9;
	}
</style>
