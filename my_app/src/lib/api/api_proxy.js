export async function apiPost(endpoint, body) {
    const res = await fetch('/api/proxy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ endpoint, body })
    });

    if (!res.ok) throw new Error(`Request failed: ${res.status}`);
    return res.json();
}

export async function apiGet(endpoint, params = {}) {
    const query = new URLSearchParams({ endpoint, ...params }).toString();
    const res = await fetch(`/api/proxy-get?${query}`);
    if (!res.ok) throw new Error(`Request failed: ${res.status}`);
    return res.json();
}
