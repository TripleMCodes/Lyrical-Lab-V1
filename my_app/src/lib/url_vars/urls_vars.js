export function get_url(){
    let url = "http://localhost:8000";
    if (process.env.NODE_ENV === 'production') {
        url = "https://m-prosody.onrender.com";
    }
    return url;

}