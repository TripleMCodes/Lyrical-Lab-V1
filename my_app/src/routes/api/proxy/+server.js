import { get_url } from '$lib/url_vars/urls_vars';

export async function POST({ request, fetch, cookies }) {
    const { endpoint, body } = await request.json();
    
    const accessToken = cookies.get('access_token');

    const res = await fetch(`${get_url()}${endpoint}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Cookie': `access_token=${accessToken}`
        },
        body: JSON.stringify(body)
    });

    const data = await res.json();
    return new Response(JSON.stringify(data), {
        status: res.status,
        headers: { 'Content-Type': 'application/json' }
    });
}