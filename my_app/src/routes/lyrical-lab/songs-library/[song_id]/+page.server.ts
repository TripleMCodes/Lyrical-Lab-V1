import type { PageServerLoad } from './$types';
import { get_url } from '$lib/url_vars/urls_vars';

export const load: PageServerLoad = async ({ fetch, params, cookies }) => {
    const { song_id } = params;
    const accessToken = cookies.get('access_token');

    const res = await fetch(`${get_url()}/api/lyric-tools/user-songs/${song_id}`, {
        headers: {
            'Accept': 'application/json',
            'Cookie': `access_token=${accessToken}`
        }
    });

    if (!res.ok) {
        console.error(`Failed to load song ${song_id}:`, res.status);
        throw new Error(`Song not found: ${res.statusText}`);
    }

    const song = await res.json();

    return {
        song,
        urls: {
            songs: true,
            writing: true
        }
    };
};