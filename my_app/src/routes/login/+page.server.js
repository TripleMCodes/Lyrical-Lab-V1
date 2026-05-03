import { fail, redirect } from '@sveltejs/kit';
import { dev } from '$app/environment';
import { get_url } from '$lib/url_vars/urls_vars';


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

        const res = await fetch(`${get_url()}/api/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: body.toString()
        });

        if (!res.ok) {
            const errorData = await res.json().catch(() => ({}));
            if (errorData.detail === 'Account is blocked') {
                throw redirect(303, '/blocked');
            }
            return fail(400, { message: 'Login failed' });
        }

        const data = await res.json();

        console.log("logging in user")


        cookies.set('access_token', data.access_token, {
            httpOnly: true,
            secure: true,
            sameSite: 'none',
            path: '/',
            maxAge: 60 * 30
            });

       
        cookies.set('refresh_token', data.refresh_token, {
            httpOnly: true,
            secure: true,
            sameSite: 'none',
            path: '/',
            maxAge: 60 * 60 * 24 * 7
            });
        
        // return { success: true };

        // Success → redirect
        throw redirect(303, '/dashboard');
    }
};
