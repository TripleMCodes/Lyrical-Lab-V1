
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
    const response = await fetch('http://localhost:8000/api/lyric-tools/user-songs',
        {
            credentials: 'include',
            headers: {
                    'Accept': 'application/json'
                }
            }
    );
    const songs = await response.json();
    
    return { 
        songs,
        logo: {
            title: 'Lyrical Lab',
            tagline: 'Login and get locked in!'
        }
    };
};