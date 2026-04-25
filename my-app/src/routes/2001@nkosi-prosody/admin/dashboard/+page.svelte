<script lang="ts">
    import AdminSettings from '$lib/components/admin/AdminSettings.svelte';
    import UserSettings from '$lib/components/admin/UserSettings.svelte';
    import SongsAdmin from '$lib/components/admin/SongsAdmin.svelte';
  

    // import type { PageData } from "../$types";
    let { data } = $props();
    // console.log(data);
    // let users = $derived.by(() => data.users || [])    let songs = $derived.by(() => data.songs || [])    // console.log(users)

    // export let data;
    // console.log(data)
    // let users = $state()
    // const { } = data;
</script>

<div class="admin-dashboard-page">
    <div class="header-row">
        <div>
            <h1>Admin dashboard</h1>
            <p>Manage admin settings and user controls in one place.</p>
        </div>
        <a class="login-link" href="/2001@nkosi-prosody/admin">Back to login</a>
    </div>

    <AdminSettings />
    <UserSettings users={data.users} />
    <SongsAdmin songs={data.totalSongs} />
</div>

<style>
    .admin-dashboard-page {
        max-width: 980px;
        margin: 0 auto;
        padding: 2rem 1rem 3rem;
        color: #111827;
    }

    .header-row {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 1rem;
        align-items: center;
        margin-bottom: 2rem;
    }

    h1 {
        margin: 0;
        font-size: clamp(2rem, 2.5vw, 2.7rem);
    }

    p {
        margin: 0.5rem 0 0;
        color: #4b5563;
        line-height: 1.6;
    }

    .login-link {
        display: inline-block;
        padding: 0.75rem 1.1rem;
        border-radius: 0.75rem;
        background: #e5e7eb;
        color: #111827;
        text-decoration: none;
        transition: background 0.2s ease;
    }

    .login-link:hover {
        background: #d1d5db;
    }
</style>
