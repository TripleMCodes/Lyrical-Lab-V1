// @ts-nocheck
import { fail } from '@sveltejs/kit';

function backendHeaders(cookies) {
  const accessToken = cookies.get('access_token');
  const refreshToken = cookies.get('refresh_token');
  let cookieHeader = '';

  if (accessToken) {
    cookieHeader += `access_token=${accessToken}`;
  }

  if (refreshToken) {
    if (cookieHeader.length > 0) cookieHeader += '; ';
    cookieHeader += `refresh_token=${refreshToken}`;
  }

  return {
    'Content-Type': 'application/json',
    Cookie: cookieHeader,
  };
}

export const load = async ({ fetch, cookies, url }) => {
    try {
        const page = url.searchParams.get('page') || 1;
        const size = url.searchParams.get('size') || 10;
        
        const msgRes = await fetch(`http://127.0.0.1:8000/api/admin/messages?page=${page}&size=${size}`, {
            method: 'GET',
            headers: backendHeaders(cookies)
        });
        const data = await msgRes.json();
        
        return {
            messages: data.items || [],
            total: data.total || 0,
            page: data.page || 1,
            size: data.size || 10,
            pages: data.pages || 1,
            next_page: data.next_page,
            prev_page: data.prev_page,
            logo: {
                title: 'Lyrical Lab',
                tagline: 'Unleash your words, craft your flow 🎤'
            },
            urls: {
                writing: false,
                login: false,
                signup: false,
                songs: false
            }
        };
    } catch (error) {
        console.error('Error fetching messages:', error);
        return {
            messages: [],
            total: 0,
            page: 1,
            size: 10,
            pages: 0,
            next_page: null,
            prev_page: null,
            logo: {
                title: 'Lyrical Lab',
                tagline: 'Unleash your words, craft your flow 🎤'
            },
            urls: {
                writing: false,
                login: false,
                signup: false,
                songs: false
            }
        };
    }
}