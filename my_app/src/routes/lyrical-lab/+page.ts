import type { PageLoad } from "../$types";
import {get_url} from "$lib/url_vars/urls_vars"

export const ssr = false;

export const load: PageLoad = async ({ fetch }) => {

    let draft_data: Object = {};

    try {
        const response = await fetch(`${get_url()}/api/lyric-tools/get-draft`, {
            method: "GET",
            credentials: "include",
        });
        if (response.ok) {
            draft_data = await response.json();
            console.log("Draft data fetched successfully:", draft_data);
        }
    } catch (error) {
        console.error("Error fetching draft data:", error);
    }

    return {
        draft_data: draft_data,
        logo: {
            title: 'M-Prosody',
            tagline: 'Drop science in the lab'
        },
        urls: {
            writing: true,
            songs:true
        }
    }
}
export const prerender = true;