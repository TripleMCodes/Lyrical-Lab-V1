import type { PageServerLoad } from './$types';
import { get_url } from '$lib/url_vars/urls_vars';

export const load: PageServerLoad = async ({ fetch, cookies }) => {
    const accessToken = cookies.get('access_token');

    const headers = {
        'Cookie': `access_token=${accessToken}`
    };

    // Fetch all endpoints in parallel
    const [res1, res2, res3, res4, res5] = await Promise.all([
        fetch(`${get_url()}/api/users/stats`, { headers }),
        fetch(`${get_url()}/api/users/song-quantity`, { headers }),
        fetch(`${get_url()}/api/users/draft`, { headers }),
        fetch(`${get_url()}/api/users/recent-songs`, { headers }),
        fetch(`${get_url()}/api/lyric-tools/get-notes`, { headers })
    ]);

    const [stats, songs_stats, draft, recent_songs, notes] = await Promise.all([
        res1.ok ? res1.json() : { writing_sessions: 0, writing_time: 0 },
        res2.ok ? res2.json() : { num_songs: 0, new_songs: 0 },
        res3.ok ? res3.json() : {},
        res4.ok ? res4.json() : [],
        res5.ok ? res5.json() : []
    ]);

    return {
        stats,
        songs_stats,
        draft,
        recent_songs,
        notes,
        logo: {
            title: 'Dashboard',
            tagline: 'See your progress over time.'
        },
        urls: {
            writing: true,
            song: true
        }
    };
};