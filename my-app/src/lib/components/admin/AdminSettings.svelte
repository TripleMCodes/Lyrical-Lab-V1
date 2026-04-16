<script>
    import { page } from '$app/stores';
    let adminName = '';
    let currentPassword = '';
    let newPassword = '';
    let confirmPassword = '';
    let apiKey = '';
    let apiUrl = '';
</script>

<section class="admin-card">
    <h2>Admin settings</h2>

    <form class="form-card" method="POST" action="?/admin_change_name">
        <label for="admin-name">Change name</label>
        <input id="admin-name" name="admin_name" type="text" bind:value={adminName} placeholder="New admin name" required />
        <button type="submit">Save name</button>
    </form>

    <form class="form-card" method="POST" action="?/admin_change_password">
        <label for="admin-old-password">Current password</label>
        <input id="admin-old-password" name="current_password" type="password" bind:value={currentPassword} placeholder="Current password" required />

        <label for="admin-new-password">New password</label>
        <input id="admin-new-password" name="new_password" type="password" bind:value={newPassword} placeholder="New password" required />

        <label for="admin-confirm-password">Confirm new password</label>
        <input id="admin-confirm-password" name="confirm_password" type="password" bind:value={confirmPassword} placeholder="Confirm password" required />

        <button type="submit">Change password</button>
    </form>

    <form class="form-card" method="POST" action="?/admin_change_api">
        <label for="admin-api-key">Change API key</label>
        <input id="admin-api-key" name="api_key" type="text" bind:value={apiKey} placeholder="New API key" />

        <label for="admin-api-url">Change API URL</label>
        <input id="admin-api-url" name="api_url" type="url" bind:value={apiUrl} placeholder="New API URL" />

        <button type="submit">Save API settings</button>
    </form>

    {#if $page.form?.message}
        <p class="message">{$page.form.message}</p>
    {/if}
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
