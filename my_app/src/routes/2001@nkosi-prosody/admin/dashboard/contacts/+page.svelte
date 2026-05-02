<script lang="ts">
    import { goto } from '$app/navigation';
    import {get_url} from "$lib/url_vars/urls_vars.js"
    let { data } = $props();
    
    let messages = $derived(data.messages);
    let currentPage = $derived(data.page);
    let totalPages = $derived(data.pages);
    let totalMessages = $derived(data.total);
    let pageSize = $derived(data.size);
    let isDeleting = $state(false);
    let showNotification = $state(false);
    let notificationMessage = $state("");
    let notificationType = $state("success");
    
    function notify(message, type = "success") {
        notificationMessage = message;
        notificationType = type;
        showNotification = true;
        setTimeout(() => {
            showNotification = false;
        }, 4000);
    }
    
    async function deleteMessage(messageId) {
        if (!confirm('Are you sure you want to delete this message?')) {
            return;
        }
        
        isDeleting = true;
        
        try {
            const res = await fetch(`${get_url()}/api/admin/messages/${messageId}`, {
                method: 'DELETE',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (res.ok) {
                notify('Message deleted successfully', 'success');
                // Reload the current page to refresh data
                await goto(`?page=${currentPage}&size=${pageSize}`);
            } else {
                const error = await res.json();
                notify(`Error: ${error.detail || 'Failed to delete message'}`, 'error');
            }
        } catch (err) {
            console.error('Delete error:', err);
            notify('Error deleting message', 'error');
        } finally {
            isDeleting = false;
        }
    }
    
    function goToPage(page) {
        if (page >= 1 && page <= totalPages) {
            goto(`?page=${page}&size=${pageSize}`);
        }
    }
    
    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
</script>

<div class="contacts-container">
    <div class="header">
        <h1>Contact Messages</h1>
        <p class="subtitle">Manage user messages and inquiries</p>
    </div>
    
    {#if showNotification}
        <div class="notification {notificationType}">
            {notificationMessage}
        </div>
    {/if}
    
    {#if messages.length === 0}
        <div class="empty-state">
            <p>No messages found</p>
        </div>
    {:else}
        <div class="messages-table">
            <div class="table-header">
                <div class="col-id">ID</div>
                <div class="col-name">Name</div>
                <div class="col-email">Email</div>
                <div class="col-subject">Subject</div>
                <div class="col-date">Date</div>
                <div class="col-actions">Actions</div>
            </div>
            
            {#each messages as message (message.id)}
                <div class="table-row">
                    <div class="col-id">{message.id}</div>
                    <div class="col-name">{message.name}</div>
                    <div class="col-email">
                        <a href="mailto:{message.email}">{message.email}</a>
                    </div>
                    <div class="col-subject">{message.subject}</div>
                    <div class="col-date">{formatDate(message.date_created)}</div>
                    <div class="col-actions">
                        <button 
                            class="btn-delete"
                            onclick={() => deleteMessage(message.id)}
                            disabled={isDeleting}
                        >
                            Delete
                        </button>
                    </div>
                </div>
                {#if message.message}
                    <div class="message-content">
                        <strong>Message:</strong>
                        <p>{message.message}</p>
                    </div>
                {:else}
                    <div class="empty-state">
                        <p>No messages found</p>
                    </div>
                {/if}
            {/each}
        </div>
        
        <div class="pagination">
            <button 
                class="btn-pagination"
                onclick={() => goToPage(1)}
                disabled={currentPage === 1}
            >
                First
            </button>
            
            <button 
                class="btn-pagination"
                onclick={() => goToPage(currentPage - 1)}
                disabled={!data.prev_page}
            >
                Previous
            </button>
            
            <div class="page-info">
                Page <input type="number" min="1" max={totalPages} bind:value={currentPage} onchange={() => goToPage(currentPage)} class="page-input"> of {totalPages}
            </div>
            
            <button 
                class="btn-pagination"
                onclick={() => goToPage(currentPage + 1)}
                disabled={!data.next_page}
            >
                Next
            </button>
            
            <button 
                class="btn-pagination"
                onclick={() => goToPage(totalPages)}
                disabled={currentPage === totalPages}
            >
                Last
            </button>
            
            <div class="page-stats">
                Total: {totalMessages} messages | Showing {(currentPage - 1) * pageSize + 1}-{Math.min(currentPage * pageSize, totalMessages)}
            </div>
        </div>
        
    {/if}
</div>

<style>
    .contacts-container {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .header {
        margin-bottom: 2rem;
    }
    
    h1 {
        font-size: 2rem;
        color: #e6ccff;
        margin: 0 0 0.5rem 0;
    }
    
    .subtitle {
        color: #b896d4;
        margin: 0;
        font-size: 0.95rem;
    }
    
    .notification {
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 6px;
        border-left: 4px solid;
    }
    
    .notification.success {
        background: rgba(76, 175, 80, 0.15);
        border-left-color: #4caf50;
        color: #90ee90;
    }
    
    .notification.error {
        background: rgba(244, 67, 54, 0.15);
        border-left-color: #f44336;
        color: #ff7675;
    }
    
    .empty-state {
        text-align: center;
        padding: 3rem;
        color: #b896d4;
        font-size: 1.1rem;
    }
    
    .messages-table {
        background: rgba(60, 0, 120, 0.1);
        border: 1px solid rgba(200, 120, 255, 0.2);
        border-radius: 8px;
        overflow: hidden;
    }
    
    .table-header {
        display: grid;
        grid-template-columns: 50px 120px 200px 200px 150px 100px;
        gap: 1rem;
        padding: 1rem;
        background: rgba(199, 125, 255, 0.1);
        border-bottom: 2px solid rgba(200, 120, 255, 0.3);
        font-weight: 600;
        color: #e0aaff;
    }
    
    .table-row {
        display: grid;
        grid-template-columns: 50px 120px 200px 200px 150px 100px;
        gap: 1rem;
        padding: 1rem;
        border-bottom: 1px solid rgba(200, 120, 255, 0.1);
        align-items: center;
        color: #d4a5ff;
    }
    
    .table-row:hover {
        background: rgba(199, 125, 255, 0.05);
    }
    
    .col-id {
        font-size: 0.85rem;
        opacity: 0.8;
    }
    
    .col-name {
        font-weight: 500;
    }
    
    .col-email a {
        color: #c77dff;
        text-decoration: none;
        border-bottom: 1px solid transparent;
        transition: all 0.2s;
    }
    
    .col-email a:hover {
        border-bottom-color: #c77dff;
    }
    
    .col-subject {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .col-date {
        font-size: 0.85rem;
        opacity: 0.8;
    }
    
    .message-content {
        grid-column: 1 / -1;
        padding: 0 1rem 1rem 1rem;
        margin-top: -0.5rem;
        border-left: 2px solid rgba(199, 125, 255, 0.2);
        padding-left: 1.5rem;
        font-size: 0.9rem;
        color: #d4a5ff;
    }
    
    .message-content p {
        margin: 0.5rem 0 0 0;
        line-height: 1.5;
        white-space: pre-wrap;
        word-break: break-word;
    }
    
    .btn-delete {
        padding: 0.4rem 0.8rem;
        background: linear-gradient(135deg, #f44336, #d32f2f);
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 0.85rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .btn-delete:hover:not(:disabled) {
        background: linear-gradient(135deg, #ff7675, #f44336);
        box-shadow: 0 0 12px rgba(244, 67, 54, 0.4);
    }
    
    .btn-delete:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
    
    .pagination {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        margin-top: 2rem;
        flex-wrap: wrap;
        padding: 1rem;
        background: rgba(60, 0, 120, 0.05);
        border-radius: 8px;
    }
    
    .btn-pagination {
        padding: 0.5rem 1rem;
        background: linear-gradient(135deg, #c77dff, #7b2cbf);
        color: white;
        border: 1px solid rgba(199, 125, 255, 0.3);
        border-radius: 6px;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .btn-pagination:hover:not(:disabled) {
        background: linear-gradient(135deg, #e0aaff, #c77dff);
        box-shadow: 0 0 12px rgba(199, 125, 255, 0.4);
    }
    
    .btn-pagination:disabled {
        opacity: 0.4;
        cursor: not-allowed;
    }
    
    .page-info {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #d4a5ff;
    }
    
    .page-input {
        width: 50px;
        padding: 0.4rem;
        background: rgba(199, 125, 255, 0.1);
        border: 1px solid rgba(199, 125, 255, 0.3);
        border-radius: 4px;
        color: #e6ccff;
        text-align: center;
        font-weight: 500;
    }
    
    .page-input:focus {
        outline: none;
        border-color: #c77dff;
        box-shadow: 0 0 8px rgba(199, 125, 255, 0.3);
    }
    
    .page-stats {
        color: #b896d4;
        font-size: 0.9rem;
    }
    
    @media (max-width: 1024px) {
        .table-header,
        .table-row {
            grid-template-columns: 40px 100px 150px 150px 120px 80px;
            gap: 0.5rem;
        }
        
        .col-subject {
            font-size: 0.8rem;
        }
    }
    
    @media (max-width: 768px) {
        .contacts-container {
            padding: 1rem;
        }
        
        h1 {
            font-size: 1.5rem;
        }
        
        .table-header,
        .table-row {
            grid-template-columns: 1fr;
        }
        
        .table-header {
            display: none;
        }
        
        .table-row {
            display: block;
            padding: 1rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(200, 120, 255, 0.2);
            border-radius: 6px;
        }
        
        .col-id,
        .col-name,
        .col-email,
        .col-subject,
        .col-date,
        .col-actions {
            display: block;
            margin-bottom: 0.5rem;
        }
        
        .col-id::before {
            content: 'ID: ';
            font-weight: 600;
            color: #e0aaff;
        }
        
        .col-name::before {
            content: 'Name: ';
            font-weight: 600;
            color: #e0aaff;
        }
        
        .col-email::before {
            content: 'Email: ';
            font-weight: 600;
            color: #e0aaff;
        }
        
        .col-subject::before {
            content: 'Subject: ';
            font-weight: 600;
            color: #e0aaff;
        }
        
        .col-date::before {
            content: 'Date: ';
            font-weight: 600;
            color: #e0aaff;
        }
        
        .pagination {
            flex-direction: column;
        }
        
        .page-stats {
            order: -1;
        }
    }
</style>