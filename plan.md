I have this function is my +page.svelte:
 // Fetch remaining requests on component mount
  async function fetchRequestsRemaining() {
    try {
      const res = await fetch(
        `${get_url()}/api/lyric-tools/api-requests-remaining`,
        {
          method: "GET",
          credentials: "include",
          headers: {
            "Content-Type": "application/json"
          }
        }
      );
      if (res.ok) {
        const data = await res.json();
        requestsRemaining = data.requests_remaining;
        maxRequests = data.max_requests_per_day;
      }
    } catch (err) {
      console.log("Error fetching requests remaining:", err);
    }
  }

I want to create a  One generic proxy endpoint, and One client-side helper function for functions like this


I think this is gonna need to be modified:
export async function apiGet(endpoint, params = {}) {
    const query = new URLSearchParams(params).toString();
    const res = await fetch(`/api/proxy-get?endpoint=${encodeURIComponent(endpoint)}&${query}`);
    if (!res.ok) throw new Error(`Request failed: ${res.status}`);
    return res.json();
}