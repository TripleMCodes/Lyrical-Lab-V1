// since there's no dynamic data here, we can prerender
// it so that it gets served as a static asset in production
export const load = () => {
	return {
		logo: {
			title: 'Lyrical Lab',
			tagline: 'Unleash your words, craft your flow 🎤'
		}
	};
};

export const prerender = true;
