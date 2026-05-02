import { writable } from 'svelte/store';

export type EditingSong = {
    song_id: string | number;
    song_name: string;
    song_genre: string;
    song_lyrics: string;
    song_artist: string;
    song_mood: string;
    song_album: string;
};

export const editingSong = writable<EditingSong | null>(null);
