<script>
    export let users = [];

    let selectedUser = '';
    let newPassword = '';
    let confirmPassword = '';
    let actionMessage = '';
    let showAll = false;

    $: userCount = users.length;

    function changePassword(event) {
        event.preventDefault();

        if (!selectedUser || !newPassword || !confirmPassword) {
            actionMessage = 'Choose a user and enter both password fields.';
            return;
        }

        if (newPassword !== confirmPassword) {
            actionMessage = 'Passwords do not match.';
            return;
        }

        actionMessage = `Password updated for ${selectedUser}.`;
        newPassword = '';
        confirmPassword = '';
    }

    function toggleBlocked(user) {
        user.blocked = !user.blocked;
        actionMessage = `${user.name} is now ${user.blocked ? 'blocked' : 'unblocked'}.`;
    }
</script>

<section class="user-card">
    <h2>User settings</h2>

    <div class="stat-row">
        <div>
            <p class="label">Number of users</p>
            <p class="value">{userCount}</p>
        </div>
        <button type="button" on:click={() => (showAll = !showAll)}>{showAll ? 'Hide all users' : 'Show all users'}</button>
    </div>

    {#if showAll}
        <div class="user-table">
            {#each users as user}
                <div class="user-row">
                    <span>{user.name}</span>
                    <span>{user.blocked ? 'Blocked' : 'Active'}</span>
                    <button type="button" on:click={() => toggleBlocked(user)}>{user.blocked ? 'Unblock' : 'Block'}</button>
                </div>
            {/each}
        </div>
    {/if}

    <form class="form-card" on:submit|preventDefault={changePassword}>
        <label for="user-select">Change password</label>
        <select id="user-select" bind:value={selectedUser}>
            <option value="">Select user</option>
            {#each users as user}
                <option value={user.name}>{user.name}</option>
            {/each}
        </select>

        <input type="password" bind:value={newPassword} placeholder="New password" />
        <input type="password" bind:value={confirmPassword} placeholder="Confirm password" />
        <button type="submit">Update password</button>
    </form>

    {#if actionMessage}
        <p class="message">{actionMessage}</p>
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
