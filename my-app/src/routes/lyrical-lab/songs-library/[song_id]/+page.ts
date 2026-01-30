import type { PageLoad } from './$types';



export const load: PageLoad = async ({ fetch, params }) => {
    const { song_id } = params;
    
    try {
        const response = await fetch(
            `http://localhost:8000/api/lyric-tools/user-songs/${song_id}`,
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
