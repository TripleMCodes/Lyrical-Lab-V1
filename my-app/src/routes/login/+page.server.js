import { fail, redirect } from '@sveltejs/kit';
import { dev } from '$app/environment';


export const actions = {
    login: async ({ request, fetch, cookies}) => {
        const formData = await request.formData();

        const email = formData.get('email');
        const password = formData.get('password');

        if (!email || !password) {
        return fail(400, { message: 'Missing email or password' });
        }

        const body = new URLSearchParams();
        // body.set('grant_type', 'password');
        body.set('username', email.toString());
        body.set('password', password.toString());

        const res = await fetch('http://127.0.0.1:8000/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: body.toString()
        });

        if (!res.ok) {
            return fail(400, { message: 'Signup failed' });
        }

        const data = await res.json();


        cookies.set('access_token', data.access_token, {
            httpOnly: true,
            secure: !dev,
            sameSite: 'lax',
            path: '/',
            maxAge: 60 * 15
            });

       
        cookies.set('refresh_token', data.refresh_token, {
            httpOnly: true,
            secure: !dev,
            sameSite: 'lax',
            path: '/',
            maxAge: 60 * 60 * 24 * 7
            });


        // Success → redirect
        throw redirect(303, '/lyrical-lab');
    }
};
