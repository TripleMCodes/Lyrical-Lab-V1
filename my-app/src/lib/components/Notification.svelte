<script>
  import { onMount, createEventDispatcher } from 'svelte';


  let {message = $bindable(), type = $bindable(), duration = $bindable(), show = $bindable()} = $props()



  let notificationElement = $state();
  const dispatch = createEventDispatcher();

  function hideNotification() {
    show = false;
    dispatch('close');
  }

  onMount(() => {
    if (show && duration > 0) {
      setTimeout(hideNotification, duration);
    }
  });

  if (show && duration > 0) {
    setTimeout(hideNotification, duration);
  }
</script>

{#if show}
  <div
    bind:this={notificationElement}
    class="notification {type}"
    class:show
    role="alert"
  >
    <span class="message">{message}</span>
    <button
      class="close-btn"
      on:click={hideNotification}
      aria-label="Close notification"
    >
      ×
    </button>
  </div>
{/if}

<style>
  .notification {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1000;
    padding: 12px 16px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    min-width: 250px;
    max-width: 400px;
    font-family: system-ui, -apple-system, sans-serif;
    font-size: 14px;
    line-height: 1.4;
    animation: slideIn 0.3s ease-out;
  }

  .notification.success {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    border: 1px solid #059669;
  }

  .notification.error {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
    border: 1px solid #dc2626;
  }

  .notification.info {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
    border: 1px solid #2563eb;
  }

  .message {
    flex: 1;
    font-weight: 500;
  }

  .close-btn {
    background: none;
    border: none;
    color: inherit;
    font-size: 18px;
    cursor: pointer;
    padding: 0;
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: background-color 0.2s ease;
  }

  .close-btn:hover {
    background-color: rgba(255, 255, 255, 0.2);
  }

  @keyframes slideIn {
    from {
      transform: translateX(100%);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }

  .notification:not(.show) {
    animation: slideOut 0.3s ease-in forwards;
  }

  @keyframes slideOut {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(100%);
      opacity: 0;
    }
  }

  @media (max-width: 480px) {
    .notification {
      left: 10px;
      right: 10px;
      min-width: auto;
    }
  }
</style>