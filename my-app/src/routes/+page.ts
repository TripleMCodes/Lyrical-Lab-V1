// since there's no dynamic data here, we can prerender
// it so that it gets served as a static asset in production
// since there's no dynamic data here, we can prerender
// it so that it gets served as a static asset in production
import type { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';



export const load:PageLoad = async () => {
	// const accessToken = cookies.get('access_token');

	// if (!accessToken) {

	// }

	
	return {
		logo: {
			title: 'Lyrical Lab',
			tagline: 'Unleash your words, craft your flow 🎤'
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
