import { fail, json, redirect } from '@sveltejs/kit';
import { get_url } from '$lib/url_vars/urls_vars.js';

export const actions = {
    signup: async ({ request, fetch }) => {
        const formData = await request.formData();

        const artist_name = formData.get('artistname');
        const age = Number(formData.get('age'));
        const password = formData.get('password');
        const confirmPassword = formData.get('confirm-password');
        const email = formData.get('email');
            

        if (!artist_name || !age || !password || !confirmPassword) {
            return fail(400, { message: 'Missing required fields' });
        }

        if (password !== confirmPassword) {
      return fail(400, { message: 'Passwords do not match' });
    }

    const res = await fetch(`${get_url()}/api/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ artist_name, age, password, email })
    });

    if (!res.ok) {
      return fail(400, { message: 'Signup failed' });
    }

    // success → redirect
    throw redirect(303, '/lyrical-lab');
  }
};