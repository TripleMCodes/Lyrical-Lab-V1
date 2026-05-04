import type { PageServerLoad } from './$types';
import { get_url } from '$lib/url_vars/urls_vars';

export const load: PageServerLoad = async ({ fetch, cookies }) => {
    let draft_data = {};
    const accessToken = cookies.get('access_token');

    try {
        const response = await fetch(`${get_url()}/api/lyric-tools/get-draft`, {
            method: 'GET',
            headers: {
                'Cookie': `access_token=${accessToken}`
            }
        });
        if (response.ok) {
            draft_data = await response.json();
        }
    } catch (error) {
        console.error('Error fetching draft data:', error);
    }

    return {
        draft_data,
        logo: { title: 'M-Prosody', tagline: 'Drop science in the lab' },
        urls: { writing: true, songs: true }
    }
}