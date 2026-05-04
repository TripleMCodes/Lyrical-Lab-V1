import type { PageServerLoad } from './$types';
import { get_url } from '$lib/url_vars/urls_vars';

export const load: PageServerLoad = async ({ fetch, params, cookies }) => {
    const { song_id } = params;
    const accessToken = cookies.get('access_token');

    const res = await fetch(`${get_url()}/api/lyric-tools/songs-library/${song_id}/versions`, {
        headers: {
            'Accept': 'application/json',
            'Cookie': `access_token=${accessToken}`
        }
    });

    if (!res.ok) {
        console.error(`Failed to fetch versions for song ${song_id}:`, res.status);
        throw new Error(`Failed to fetch song versions: ${res.statusText}`);
    }

    const versions = await res.json();

    return {
        versions,
        urls: { songs: true, writing: true, sigup: false, login: false }
    };
};