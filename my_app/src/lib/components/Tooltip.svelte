<script>
    let {text} = $props();


</script>

<span class="tooltip">
  <slot />
  <span class="tooltip-text">{text}</span>
</span>

<style>
    .tooltip {
        position: relative;
        display: inline-flex;
        }

.tooltip-text {
    position: absolute;
    bottom: -2.2rem;
    left: 50%;
    transform: translateX(-50%);
    background: #111;
    color: white;
    padding: 0.35rem 0.6rem;
    font-size: 0.75rem;
    border-radius: 0.4rem;
    opacity: 0;
    white-space: nowrap;
    transition: opacity 0.15s ease;
    pointer-events: none;
    }

    .tooltip:hover .tooltip-text {
        opacity: 1;
    }

</style>

