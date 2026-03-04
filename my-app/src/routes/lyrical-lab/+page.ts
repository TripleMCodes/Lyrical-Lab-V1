import type { PageLoad } from "../$types";

export const ssr = false;

export const load: PageLoad = async ({ fetch }) => {

    let draft_data: Object = {};

    try {
        const response = await fetch('http://localhost:8000/api/lyric-tools/get-draft', {
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
            title: 'Lyrical Lab',
            tagline: 'Drop science in the lab'
        },
        urls: {
            writing: true,
            songs:true
        }
    }
}
export const prerender = true;