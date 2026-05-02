<script lang="ts">
    import { page } from '$app/stores';
    // export let users = [];

    let { users = $bindable() } = $props()

    let selectedUser = $state("")
    let newPassword = $state("");
    let confirmPassword = $state("");
    let showAll = $state(false);

    let userCount = $state(users.length);
</script>

<section class="user-card">
    <h2>User settings</h2>

    <div class="stat-row">
        <div>
            <p class="label">Number of users</p>
            <p class="value">{userCount}</p>
        </div>
        <button type="button" onclick={() => (showAll = !showAll)}>{showAll ? 'Hide all users' : 'Show all users'}</button>
    </div>

    {#if showAll}
        <div class="user-table">
            {#each users as user}
                <div class="user-row">
                    <span>{user.artist_name}</span>
                    <span>{user.blocked ? 'Blocked' : 'Active'}</span>
                    <form method="POST" action="?/admin_toggle_user_block">
                        <input type="hidden" name="user_id" value={user.uid} />
                        <input type="hidden" name="blocked" value={!user.blocked} />
                        <button type="submit">{user.blocked ? 'Unblock' : 'Block'}</button>
                    </form>
                </div>
            {/each}
        </div>
    {/if}

    <form class="form-card" method="POST" action="?/admin_change_user_password">
        <label for="user-select">Change password</label>
        <select id="user-select" name="user_id" bind:value={selectedUser} required>
            <option value="">Select user</option>
            {#each users as user}
                <option value={user.uid}>{user.artist_name}</option>
            {/each}
        </select>

        <input name="new_password" type="password" bind:value={newPassword} placeholder="New password" required />
        <input name="confirm_password" type="password" bind:value={confirmPassword} placeholder="Confirm password" required />
        <button type="submit">Update password</button>
    </form>

    {#if $page.form?.message}
        <p class="message">{$page.form.message}</p>
    {/if}
</section>

<style>
    .user-card {
        border-radius: 1rem;
        background: #ffffff;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
        padding: 1.5rem;
    }

    .user-card h2 {
        margin-bottom: 1rem;
    }

    .stat-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .label {
        font-size: 0.95rem;
        color: #4b5563;
    }

    .value {
        font-size: 1.4rem;
        font-weight: 700;
        margin-top: 0.25rem;
    }

    .user-table {
        border: 1px solid #e5e7eb;
        border-radius: 0.75rem;
        overflow: hidden;
        margin-bottom: 1rem;
    }

    .user-row {
        display: grid;
        grid-template-columns: 1.5fr 1fr auto;
        gap: 1rem;
        align-items: center;
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #e5e7eb;
    }

    .user-row:last-child {
        border-bottom: none;
    }

    .user-row button {
        padding: 0.65rem 1rem;
        border: none;
        border-radius: 0.65rem;
        background: #2563eb;
        color: white;
        cursor: pointer;
    }

    .user-row button:hover {
        background: #1d4ed8;
    }

    .form-card {
        display: grid;
        gap: 0.75rem;
    }

    select,
    input {
        width: 100%;
        border: 1px solid #d1d5db;
        border-radius: 0.5rem;
        padding: 0.75rem;
    }

    button[type="submit"],
    .stat-row button {
        width: fit-content;
        padding: 0.8rem 1.2rem;
        border: none;
        border-radius: 0.65rem;
        background: #2563eb;
        color: white;
        cursor: pointer;
    }

    button[type="submit"]:hover,
    .stat-row button:hover {
        background: #1d4ed8;
    }

    .message {
        color: #1f2937;
        font-size: 0.95rem;
    }
</style>
