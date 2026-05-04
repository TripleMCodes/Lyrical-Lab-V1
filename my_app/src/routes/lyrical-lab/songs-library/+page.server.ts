import type { PageServerLoad } from './$types';
import { get_url } from '$lib/url_vars/urls_vars';

const DEFAULT_PAGE = 1;
const DEFAULT_SIZE = 4;

export const load: PageServerLoad = async ({ fetch, url, cookies }) => {
    const page = Number(url.searchParams.get('page')) || DEFAULT_PAGE;
    const size = Number(url.searchParams.get('size')) || DEFAULT_SIZE;
    const accessToken = cookies.get('access_token');

    const endpoint = new URL(`${get_url()}/api/lyric-tools/user-songs`);
    endpoint.searchParams.set('page', String(page));
    endpoint.searchParams.set('size', String(size));

    try {
        const res = await fetch(endpoint.toString(), {
            headers: {
                'Cookie': `access_token=${accessToken}`
            }
        });

        if (!res.ok) {
            console.error('user-songs failed', res.status);
            return defaultReturn(page, size);
        }

        const data = await res.json();

        return {
            songs: data.items ?? [],
            meta: {
                page: data.page ?? page,
                size: data.size ?? size,
                total: data.total ?? 0,
                pages: data.pages ?? 1,
                next_page: data.next_page ?? null,
                prev_page: data.prev_page ?? null
            },
            urls: {
                writing: true,
                songs: true
            }
        };

    } catch (error) {
        console.error('Error fetching user songs:', error);
        return defaultReturn(page, size);
    }
};

function defaultReturn(page: number, size: number) {
    return {
        songs: [],
        meta: { page, size, total: 0, pages: 1, next_page: null, prev_page: null },
        urls: { writing: true, songs: true }
    };
}