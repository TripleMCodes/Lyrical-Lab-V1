
import type { PageLoad } from './$types';

export const ssr = false;
export const prerender = false;

const DEFAULT_PAGE = 1;
const DEFAULT_SIZE = 4;

export const load: PageLoad = async ({ fetch, url }) => {
  const page = Number(url.searchParams.get('page')) || DEFAULT_PAGE;
  const size = Number(url.searchParams.get('size')) || DEFAULT_SIZE;

  const endpoint = new URL('http://localhost:8000/api/lyric-tools/user-songs');
  endpoint.searchParams.set('page', String(page));
  endpoint.searchParams.set('size', String(size));

  const res = await fetch(endpoint.toString(), { credentials: 'include' });

  if (!res.ok) {
    console.error('user-songs failed', res.status);
    return {
      songs: [],
      meta: { page, size, total: 0, pages: 1, next_page: null, prev_page: null }
    };
  }

const data = await res.json();
// console.log("data:", data);
// console.log("data.items:", data.items);
// console.log("data.debug:", data.debug);

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
    
  }
  ;
};








