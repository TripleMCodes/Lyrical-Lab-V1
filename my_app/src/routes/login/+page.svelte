<script lang="ts">
    import '../signup/sigup.css';
    import { enhance } from '$app/forms';
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';

    
    import { applyAction } from '$app/forms';

    const enhanceForm = () => {
        return async ({ result, update }: any) => {
            if (result?.type === 'success') {
                await goto('/lyrical-lab');
            } else {
                await applyAction(result);
            }
        };
    };

    let email = $state("");
    let password = $state("");
</script>

<div class="container">
    <div class="login-container">
        <h1>Login</h1>

        {#if $page.form?.message}
            <div class="signup bg-amber-50">
                <p class="error">{$page.form.message}</p>
            </div>
        {/if}

        <form class="login-form" method="POST" action="?/login" use:enhance={enhanceForm}>
            <div class="login-group">
                <label for="email">Email</label>
                <input
                    type="email" 
                    id="email"
                    name="email"
                    placeholder="Enter your email"
                    required
                    bind:value={email}
                >
            </div>

            <div class="login-group">
                <label for="password">Password</label>
                <input
                    type="password"
                    id="password"
                    name="password"
                    placeholder="Enter password"
                    required
                    bind:value={password}
                >
            </div>

            <button type="submit">Login</button>
        </form>

        <p class="signup-link">
            Don't have an account? <a href="/signup">Signup</a>
        </p>
    </div>
</div>