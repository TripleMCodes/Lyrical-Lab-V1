export function get_url(){
    let url = "https://m-prosody.onrender.com";
    if (process.env.NODE_ENV === 'production') {
        url = "https://m-prosody.onrender.com";
    }
    // let url = "http://192.168.0.194:8000"
    return url;

}