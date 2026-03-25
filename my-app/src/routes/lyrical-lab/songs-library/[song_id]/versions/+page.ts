import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, params }) => {
    const { song_id } = params;

    console.log('Loading versions for song_id:', song_id); // Debug log

    
    try { 
        const response = await fetch(`http://localhost:8000/api/lyric-tools/songs-library/${song_id}/versions`, {
            credentials: 'include',
            headers: {
                'Accept': 'application/json'
            }
        });
        if (!response.ok) {
            throw new Error(`Failed to fetch song versions: ${response.statusText}`);
        }  
        const versions = await response.json();
        console.log("song data", versions)

        return {
            versions,
            urls: {songs: true, writing: true, sigup: false, login: false}
        };
    } catch (error) {
        console.error('Error fetching song versions:', error);
        throw new Error('Failed to fetch song versions');
    }
};