import type { PageLoad } from "../$types";
import {get_url} from "$lib/url_vars/urls_vars"

export const ssr = false;

export const load: PageLoad = async ({ fetch }) => {
    let stats_data: Object = {
        writing_sessions: 0,
        writing_time: 0
    };

    let songs_data: Object = {
        "num_songs": 0,
        "new_songs": 0
    }

    let song_draft:Object = {}

    let recent_songs_data:Array<Object> = []

    let notes_data: Array<Object> = []
    
    const res = await fetch(`${get_url()}/api/users/stats`, {
        method: "GET",
        credentials: "include",
    });

    const res2 = await fetch(`${get_url()}/api/users/song-quantity`, {
        method: "GET",
        credentials: "include"
    });

    const res3 = await fetch(`${get_url()}/api/users/draft`, {
        method: "GET",
        credentials: "include"
    });

    const res4 = await fetch(`${get_url()}/api/users/recent-songs`, {
        method: "GET",
        credentials: "include"
    });

    const res5 = await fetch(`${get_url()}/api/lyric-tools/get-notes`, {
        method: "GET",
        credentials: "include"
    });

    if (res.ok) {
        stats_data = await res.json();
    }

    if (res2.ok) {
        songs_data = await res2.json()
    }

    if (res3.ok) {
        song_draft  = await res3.json()
    } else {
        song_draft = res3.json()
    }

    if (res4.ok) {
        recent_songs_data = await res4.json()
    }

    if (res5.ok) {
        notes_data = await res5.json()
    }

    

    return {
        stats: stats_data,
        songs_stats: songs_data,
        recent_songs: recent_songs_data,
        draft: song_draft, 
        notes: notes_data,
        logo: {
            title: "Dashboard",
            tagline: "See your progress over time."
        },
        urls: {
            writing: true,
            song: true
        }
    };
};

export const prerender = true;
