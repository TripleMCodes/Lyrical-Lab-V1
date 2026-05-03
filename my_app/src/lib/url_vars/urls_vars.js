export function get_url(){
    let url = "https://m-prosody.onrender.com";
    if (process.env.NODE_ENV === 'production') {
        url = "https://m-prosody.onrender.com";
    }
    return url;

}