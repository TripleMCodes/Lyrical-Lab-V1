<script>
    import '../../signup/sigup.css'
    import { enhance } from '$app/forms'
    import { page } from '$app/stores'

    let username = $state("")
    let password = $state("")
</script>

<div class="container">
    <div class="login-container">
        <h1>Admin Login</h1>

        {#if $page.form?.message}
            <div class="signup bg-amber-50">
                <p class="error">{$page.form.message}</p>
            </div>
        {/if}

        <form class="login-form" method="POST" action="?/admin_login" use:enhance >
            <div class="login-group">
                <label for="username">Admin Name</label>
                <input type="text" id="username" name="username" placeholder="Enter admin name" required bind:value={username}>
            </div>

            <div class="login-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" placeholder="Enter password" required bind:value={password}>
            </div>

            <button type="submit">Login</button>
        </form>
    </div>
</div>
