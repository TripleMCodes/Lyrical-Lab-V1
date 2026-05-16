import type { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';



export const load:PageLoad = async () => {
	
	return {
		logo: {
			title: 'M-Prosody',
			tagline: 'Unleash your words, craft your flow!'
		},
		urls: {
			writing: false,
			login: true,
			signup: true,
			songs: false
        }
	};
};

export const prerender = true;
