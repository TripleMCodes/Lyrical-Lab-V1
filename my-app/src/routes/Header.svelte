<script>
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
</script>

<header>
	<div class="logo-container">
    	<img src="/logo_no_bg.png" alt="M-Prosody logo" class="logo-1">
	</div>
	<div class="logo">
		<h1>{'/ɛm ˈprɑːsədi/'}</h1>
		<p>{page.data.logo?.tagline}</p>
	</div>


	<div class="nav-container">
		<nav>
			<ul>
				<li aria-current={page.url.pathname === '/' ? 'page' : undefined}>
					<a href={resolve('/')}>Home</a>
				</li>
				<!-- <li aria-current={page.url.pathname === '/about' ? 'page' : undefined}>
					<a href={resolve('/about')}>About</a>
				</li> -->
				<!-- <li aria-current={page.url.pathname.startsWith('/sverdle') ? 'page' : undefined}>
					<a href={resolve('/sverdle')}>Sverdle</a>
				</li> -->
				{#if page.data?.urls?.signup}
				<li aria-current={page.url.pathname === '/signup' ? 'page' : undefined}>
					<a href={resolve('/signup')}>Signup</a>
				</li>
				{/if}
				{#if page.data?.urls?.login}
					<li aria-current={page.url.pathname === '/login' ? 'page' : undefined}>
						<a href={resolve('/login')}>Login</a>
					</li>
				{/if}
				{#if page.data?.urls?.writing}
					<li aria-current={page.url.pathname === '/lyrical-lab' ? 'page' : undefined}>
					<a href={resolve('/lyrical-lab')}>Writing Studio</a>
					</li>
				{/if}
				{#if page.data?.urls?.writing}
					<li aria-current={page.url.pathname === '/dashboard' ? 'page' : undefined}>
					<a href={resolve('/dashboard')}>Dashboard</a>
					</li>
				{/if}
				{#if page.data?.urls?.songs}
				<li aria-current={page.url.pathname === '/lyrical-lab/songs-library' ? 'page' : undefined}>
					<a href={`${resolve('/lyrical-lab/songs-library')}?page=1&size=4`}>Songs</a>
				</li>
				{/if}
				<li aria-current={page.url.pathname === '/public-rhyme-engine'}>
					<a href={`${resolve('/public-rhyme-engine')}`}>Rhyme Api</a>
				</li>


			</ul>
		</nav>
	</div>


</header>

