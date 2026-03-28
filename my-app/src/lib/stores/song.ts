import { writable } from 'svelte/store';
import type { EditingSong } from './editingSong';

export const currentSong = writable<EditingSong | null>(null);