import { redirect } from '@sveltejs/kit';
import { dev } from '$app/environment';

export async function handle({ event, resolve }) {
  const accessToken = event.cookies.get('access_token');
  const refreshToken = event.cookies.get('refresh_token');

  //
  if (!accessToken && !refreshToken) {
    return resolve(event);
  }

  //try request normally
  let response = await resolve(event);

  //if access token expired
  if (response.status === 401 && refreshToken) {
    const refreshRes = await fetch('http://localhost:8000/api/refresh', {
      method: 'POST',
      headers: {
        Cookie: `refresh_token=${refreshToken}`
      }
    });

    if (!refreshRes.ok) {
      
      event.cookies.delete('access_token', { path: '/' });
      event.cookies.delete('refresh_token', { path: '/' });
      throw redirect(303, '/login');
    }

    const data = await refreshRes.json();

    
    event.cookies.set('access_token', data.access_token, {
      httpOnly: true,
      sameSite: 'none',
      secure: true,
      path: '/',
      maxAge: 60 * 15
    });

    //retrying og req
    response = await resolve(event);
  }

  return response;
}
