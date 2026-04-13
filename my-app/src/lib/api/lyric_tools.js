export async function fetchRhymes(word) {
    let url = `http://localhost:8000/api/lyric-tools/find-rhymes`;

    console.log("rhyme query ", word)
    try {
        const res = await fetch(
            url,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({"word": word})
            }

        )

        if (res.ok) {
            return res.json()
        }
        else {
            return {"message": `Error - couldn't fetch rhymes for ${word}`}
        }
    } catch (err) {
        return err
    }
}



export async function searchLyrics(query, topK = 5) {
    let url = `http://localhost:8000/api/lyrics-search/?q=${encodeURIComponent(query)}&top_k=${topK}`;

    try {
        const res = await fetch(url, {
            method: "GET",
            credentials: "include",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (res.ok) {
            const data = await res.json();
            return data;
        } else {
            const error = await res.json();
            throw new Error(error.detail || `Search failed: ${res.status}`);
        }
    } catch (err) {
        console.error("Search error:", err);
        throw err;
    }
} 