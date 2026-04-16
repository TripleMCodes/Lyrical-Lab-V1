<script>
    let adminName = '';
    let oldPassword = '';
    let newPassword = '';
    let confirmPassword = '';
    let apiKey = '';
    let apiUrl = '';
    let nameMessage = '';
    let passwordMessage = '';
    let apiMessage = '';

    function updateName(event) {
        event.preventDefault();
        nameMessage = adminName.trim()
            ? `Admin name changed to “${adminName.trim()}”`
            : 'Please enter a valid admin name.';
    }

    function updatePassword(event) {
        event.preventDefault();

        if (!oldPassword || !newPassword || !confirmPassword) {
            passwordMessage = 'Fill in all password fields.';
            return;
        }

        if (newPassword !== confirmPassword) {
            passwordMessage = 'New passwords do not match.';
            return;
        }

        passwordMessage = 'Admin password updated successfully.';
        oldPassword = '';
        newPassword = '';
        confirmPassword = '';
    }

    function updateApi(event) {
        event.preventDefault();
        apiMessage = apiKey.trim() || apiUrl.trim()
            ? 'Admin API settings saved.'
            : 'Enter a new API key or API URL to save.';
    }
</script>

<section class="admin-card">
    <h2>Admin settings</h2>

    <form class="form-card" on:submit|preventDefault={updateName}>
        <label for="admin-name">Change name</label>
        <input id="admin-name" type="text" bind:value={adminName} placeholder="New admin name" />
        <button type="submit">Save name</button>
        {#if nameMessage}
            <p class="message">{nameMessage}</p>
        {/if}
    </form>

    <form class="form-card" on:submit|preventDefault={updatePassword}>
        <label for="admin-old-password">Current password</label>
        <input id="admin-old-password" type="password" bind:value={oldPassword} placeholder="Current password" />

        <label for="admin-new-password">New password</label>
        <input id="admin-new-password" type="password" bind:value={newPassword} placeholder="New password" />

        <label for="admin-confirm-password">Confirm new password</label>
        <input id="admin-confirm-password" type="password" bind:value={confirmPassword} placeholder="Confirm password" />

        <button type="submit">Change password</button>
        {#if passwordMessage}
            <p class="message">{passwordMessage}</p>
        {/if}
    </form>

    <form class="form-card" on:submit|preventDefault={updateApi}>
        <label for="admin-api-key">Change API key</label>
        <input id="admin-api-key" type="text" bind:value={apiKey} placeholder="New API key" />

        <label for="admin-api-url">Change API URL</label>
        <input id="admin-api-url" type="url" bind:value={apiUrl} placeholder="New API URL" />

        <button type="submit">Save API settings</button>
        {#if apiMessage}
            <p class="message">{apiMessage}</p>
        {/if}
    </form>
</section>

<style>
    .admin-card {
        border-radius: 1rem;
        background: #ffffff;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .admin-card h2 {
        margin-bottom: 1rem;
    }

    .form-card {
        display: grid;
        gap: 0.75rem;
        margin-bottom: 1.25rem;
        padding: 1rem;
        border: 1px solid #e5e7eb;
        border-radius: 0.75rem;
    }

    label {
        font-weight: 600;
    }

    input {
        border: 1px solid #d1d5db;
        border-radius: 0.5rem;
        padding: 0.75rem;
        width: 100%;
    }

    button {
        width: fit-content;
        padding: 0.8rem 1.2rem;
        border: none;
        border-radius: 0.65rem;
        background: #2563eb;
        color: white;
        cursor: pointer;
    }

    button:hover {
        background: #1d4ed8;
    }

    .message {
        color: #1f2937;
        font-size: 0.95rem;
    }
</style>
