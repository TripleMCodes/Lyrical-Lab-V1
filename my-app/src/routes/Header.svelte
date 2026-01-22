<script>
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import logo from '$lib/images/svelte-logo.svg';
	import github from '$lib/images/github.svg';
</script>

<header>
	<div class="logo">
		<h1>{page.data.logo?.title ?? 'Lyrical Lab'}</h1>
		<p>{page.data.logo?.tagline}</p>
	</div>


	<div class="nav-container">
		<nav>
			<ul>
				<li aria-current={page.url.pathname === '/' ? 'page' : undefined}>
					<a href={resolve('/')}>Home</a>
				</li>
				<li aria-current={page.url.pathname === '/about' ? 'page' : undefined}>
					<a href={resolve('/about')}>About</a>
				</li>
				<li aria-current={page.url.pathname.startsWith('/sverdle') ? 'page' : undefined}>
					<a href={resolve('/sverdle')}>Sverdle</a>
				</li>
				{#if page.data.urls.signup}
				<li aria-current={page.url.pathname === '/signup' ? 'page' : undefined}>
					<a href={resolve('/signup')}>Signup</a>
				</li>
				{/if}
				{#if page.data.urls.login}
					<li aria-current={page.url.pathname === '/login' ? 'page' : undefined}>
						<a href={resolve('/login')}>Login</a>
					</li>
				{/if}
				{#if page.data.urls.writing}
					<li aria-current={page.url.pathname === '/lyrical-lab' ? 'page' : undefined}>
					<a href={resolve('/lyrical-lab')}>Writing Studio</a>
					</li>
				{/if}
				{#if page.data.urls.songs}
					<li aria-current={page.url.pathname === '/lyrical-lab/songs-library' ? 'page' : undefined}>
					<a href={resolve('/lyrical-lab/songs-library')}>Songs</a>
					</li>
				{/if}

			</ul>
		</nav>
	</div>


</header>

<style>
	/* .logo{
		display:flex;
		align-items: center;
		justify-content: center;
		flex-direction: column;
	}
	.nav-container{
		display:flex;
		align-items: center;
		justify-content: center;
		flex-direction: column;
	} */

	/* .corner {
		width: 3em;
		height: 3em;
	}

	.corner a {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100%;
	}

	.corner img {
		width: 2em;
		height: 2em;
		object-fit: contain;
	} */

	 /* nav {
		display: flex;
		justify-content: center;
		--background: rgba(255, 255, 255, 0.7);
	}

	svg {
		width: 2em;
		height: 3em;
		display: block;
	}

	path {
		fill: var(--background);
	}

	ul {
		position: relative;
		padding: 0;
		margin: 0;
		height: 3em;
		display: flex;
		justify-content: center;
		align-items: center;
		list-style: none;
		background: var(--background);
		background-size: contain;
	}

	li {
		position: relative;
		height: 100%;
	}

	li[aria-current='page']::before {
		--size: 6px;
		content: '';
		width: 0;
		height: 0;
		position: absolute;
		top: 0;
		left: calc(50% - var(--size));
		border: var(--size) solid transparent;
		border-top: var(--size) solid var(--color-theme-1);
	}

	nav a {
		display: flex;
		height: 100%;
		align-items: center;
		padding: 0 0.5rem;
		color: var(--color-text);
		font-weight: 700;
		font-size: 0.8rem;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		text-decoration: none;
		transition: color 0.2s linear;
	}

	a:hover {
		color: var(--color-theme-1);
	} */
</style> 
