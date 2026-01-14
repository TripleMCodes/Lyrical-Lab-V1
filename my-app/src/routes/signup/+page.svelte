<script>
    import './sigup.css'
    import { enhance } from '$app/forms';
    import { page } from '$app/stores';

    let artist_name = $state("")
    let email = $state("")
    let age = $state("");
    let password = $state("")
    let confirmPassword = $state("")

</script>


<div class="container">
     <div class="signup-container">
        <h1>Create an Account</h1>

        {#if $page.form?.message}
            <div class="signup bg-amber-50">
                <p class="error">{$page.form.message}</p>
            </div>

        {/if}

        <form class="signup-form" method="POST" action="?/signup" use:enhance >

      <div class="form-group">
        <label for="name">Artist Name</label>
        <input type="text" id="artistname" name="artistname" placeholder="Enter your artist name" required bind:value={artist_name}>
      </div>

      <div class="form-group">
        <label for="email">Email</label>
        <input type="text" id="email" name="email" placeholder="Enter your email address" required bind:value={email}>
      </div>

      <div class="form-group">
        <label for="age">Age</label>
        <input type="number" id="age" name="age" placeholder="Enter your age" min="13" required bind:value={age}>
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" name="password" placeholder="Enter password" required bind:value={password}>
      </div>

      <div class="form-group">
        <label for="confirm-password">Confirm Password</label>
        <input type="password" id="confirm-password" name="confirm-password" placeholder="Re-enter password" required bind:value={confirmPassword}>
      </div>

      <button type="submit">Sign Up</button>
    </form>

    <p class="login-link">Already have an account? <a href="/login">Login</a></p>

     </div>
</div>

