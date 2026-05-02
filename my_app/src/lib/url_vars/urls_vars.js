export function get_url(){
    let url = "http://localhost:8000";
    if (process.env.NODE_ENV === 'production') {
        url = "https://wordy-backend.onrender.com";
    }
    return url;

}