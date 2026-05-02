<script>
	export let text = 'Invoking...';
</script>

<div class="sigil-wrapper" aria-live="polite">
	<div class="sigil">
		<span class="ring"></span>
		<span class="ring"></span>
		<span class="core"></span>
	</div>
	<p class="sigil-text">{text}</p>
</div>

<style>
	.sigil-wrapper {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 2.5rem;
		color: #d8b3ff;
	}

	/* --- SIGIL STRUCTURE --- */

	.sigil {
		position: relative;
		width: 64px;
		height: 64px;
		margin-bottom: 1.2rem;
	}

	.ring {
		position: absolute;
		inset: 0;
		border-radius: 50%;
		border: 2px solid transparent;
		border-top-color: #a855f7;
		border-bottom-color: #7c3aed;
		box-shadow: 0 0 14px rgba(168, 85, 247, 0.7);
		animation: rotate 2.2s linear infinite;
	}

	.ring:nth-child(2) {
		inset: 8px;
		border-top-color: #c084fc;
		border-bottom-color: #9333ea;
		animation-direction: reverse;
		animation-duration: 3.2s;
	}

	.core {
		position: absolute;
		inset: 22px;
		border-radius: 4px;
		background: #d8b3ff;
		box-shadow:
			0 0 8px #d8b3ff,
			0 0 16px rgba(168, 85, 247, 0.8);
		animation: pulse 1.8s ease-in-out infinite;
	}

	/* --- TEXT --- */

	.sigil-text {
		font-family: 'Fira Mono', monospace;
		font-size: 0.85rem;
		opacity: 0.85;
		letter-spacing: 0.05em;
		text-shadow: 0 0 8px rgba(168, 85, 247, 0.7);
	}

	/* --- ANIMATIONS --- */

	@keyframes rotate {
		from {
			transform: rotate(0deg);
		}
		to {
			transform: rotate(360deg);
		}
	}

	@keyframes pulse {
		0% {
			transform: scale(0.85);
			opacity: 0.6;
		}
		50% {
			transform: scale(1);
			opacity: 1;
		}
		100% {
			transform: scale(0.85);
			opacity: 0.6;
		}
	}
</style>
