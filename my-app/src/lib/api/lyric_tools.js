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