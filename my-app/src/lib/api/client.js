
export async function fetchWords(type, word) {
    let url = '';
    // word = word.toLowerCase();
    console.log('the type and word ', word, type)
    switch (type) {
        case "rhyme":
            url = `https://api.datamuse.com/words?rel_rhy=${word}`;
            break;
        case "synonym":
            url = `https://api.datamuse.com/words?rel_syn=${word}`;
            break;
        case "related":
            url = `https://api.datamuse.com/words?rel_trg=${word}`;
            break;
        case "homophone":
            url = `https://api.datamuse.com/words?rel_hom=${word}`;
            break;
        default:
            console.error("Unsupported type:", type);
            return [];
    }

    let res = await fetch(url);
    if (!res.ok) {
        console.error("HTTP Error:", res.status);
        return [];
    }

    let data = await res.json();
    // console.log(data);
    return data;
}