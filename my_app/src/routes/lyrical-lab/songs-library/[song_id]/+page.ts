import type { PageLoad } from './$types';
import {get_url} from "$lib/url_vars/urls_vars"


export const load: PageLoad = async ({ fetch, params }) => {
    const { song_id } = params;
    
    try {
        const response = await fetch(
            `${get_url()}/api/lyric-tools/user-songs/${song_id}`,
            {
                credentials: 'include',
                headers: {
                    'Accept': 'application/json'
                }
            }
        );
        
        if (!response.ok) {
            throw new Error(`Song not found: ${response.statusText}`);
        }
        
        const song = await response.json();
        console.log('Fetched song:', song);
        
        return {
            song,
            urls:{
                songs: true,
                writing: true
            }
        };
    } catch (error) {
        console.error('Failed to load song:', error);
        throw new Error('Failed to load song');
    }
};
