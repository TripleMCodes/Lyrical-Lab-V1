I have fixed how I set CORS:

origins = [
    "http://localhost:5173",
    "https://m-prosody.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # explicit list, no wildcard
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

backend logs:
INFO:     102.251.68.13:0 - "OPTIONS /api/lyric-tools/find-rhymes HTTP/1.1" 200 OK
INFO:     102.252.68.25:0 - "POST /api/lyric-tools/find-rhymes HTTP/1.1" 422 Unprocessable Content


response:
B8ogjULU.js:1 
 POST https://m-prosody.onrender.com/api/lyric-tools/save-writing-seconds 422 (Unprocessable Content)
window.fetch	@	B8ogjULU.js:1
D	@	13.CRr-bj_h.js:1
z	@	13.CRr-bj_h.js:1
N	@	13.CRr-bj_h.js:1

This is my +page.server.js when I log in:
import { fail, redirect } from '@sveltejs/kit';
import { get_url } from '$lib/url_vars/urls_vars';

export const actions = {
    login: async ({ request, fetch, cookies }) => {
        const formData = await request.formData();

        const email = formData.get('email');
        const password = formData.get('password');

        if (!email || !password) {
            return fail(400, { message: 'Missing email or password' });
        }

        const body = new URLSearchParams();
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

        return { success: true };
    }
};
