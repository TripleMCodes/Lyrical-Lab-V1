Here is my backend function that does the rhyme search:


@router.post('/find-rhymes')
def find_rhymes(
    data: dict,
    current_user: models.Users = Depends(oauth2.get_current_user)
):
    word = data["word"]
    word_rhymes_list = []
    phrasal_rhymes_list = []

    logging.debug(f"the data is {data}")
    logging.debug(f"the word is {word}") 
    
    try:
        results = find_rhymes_api(word)
        
        # Extract word rhymes from dictionary
        if "word_rhymes" in results and isinstance(results["word_rhymes"], dict):
            for input_word, rhymes in results["word_rhymes"].items():
                for rhyme_word, score in rhymes:
                    word_rhymes_list.append({
                        "word": rhyme_word,
                        "score": score,
                        "type": "word",
                        "input_word": input_word
                    })
        
        # Extract phrasal rhymes
        if "phrasal_rhymes" in results and isinstance(results["phrasal_rhymes"], list):
            for phrasal_rhyme, score in results["phrasal_rhymes"]:
                phrasal_rhymes_list.append({
                    "phrase": phrasal_rhyme,
                    "score": score,
                    "type": "phrasal"
                })
        
        # Sort by score (highest first)
        word_rhymes_list.sort(key=lambda x: x["score"], reverse=True)
        phrasal_rhymes_list.sort(key=lambda x: x["score"], reverse=True)
        
        # Combine results
        combined_results = {
            "word_rhymes": word_rhymes_list,
            "phrasal_rhymes": phrasal_rhymes_list,
            "total_word_rhymes": len(word_rhymes_list),
            "total_phrasal_rhymes": len(phrasal_rhymes_list)
        }
        
        logging.debug(f"Word rhymes found: {len(word_rhymes_list)}, Phrasal rhymes found: {len(phrasal_rhymes_list)}")
        return combined_results
        
    except Exception as e:
        logging.debug(e)
        return {'error': "Error - Please check word and ensure it is not multi-phrasal."}


Here is the function at the front that makes a request to this route:
import { get_url } from "$lib/url_vars/urls_vars";

export async function fetchRhymes(word) {
    let url = `${get_url()}/api/lyric-tools/find-rhymes`;

    console.log("rhyme query ", word)
    try {
        const res = await fetch(
            url,
            {
                method: "POST",
                credentials: "include",
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

This is where the function is used in the +page.svelte:
async function fetchWordsWrapper(){
    isLoading = true
    console.log("Fetch ", wordSelected)
    if (wordSelected === "rhyme"){
      console.log("the rhyme is ", wordSearched)
      const data = await fetchRhymes(wordSearched)
      console.log('Rhyme data:', data)
      
      // Handle new rhyme response format with word_rhymes and phrasal_rhymes
      let combinedList = []
      
      if (data.phrasal_rhymes) {
        combinedList.push(...data.phrasal_rhymes.map(item => ({
          word: item.phrase,
          score: item.score,
          type: 'phrasal'
        })))
      }
      if (data.word_rhymes) {
        combinedList.push(...data.word_rhymes.map(item => ({
          word: item.word,
          score: item.score,
          type: 'word',
          input_word: item.input_word
        })))
      }
      
      
      wordList = combinedList
      
      if (wordList.length === 0){
        notificationMessage = "No rhymes found";
        notificationType = "error";
        showNotification = true;
        isLoading = false
      }
    }else{
      const lst = await fetchWords(wordSelected, wordSearched)
      wordList = lst
      console.log($state.snapshot(wordList))
      if (wordList.length === 0){
        notificationMessage = "No results found";
        notificationType = "error";
        showNotification = true;
        isLoading = false
      }
    }

    let textList = ""
    isLoading = false
    for (let index = 0; index < wordList.length; index++) {
      const item = wordList[index]
      // const score = item.score ? ` (${item.score.toFixed(2)})` : ''
      // const typeLabel = item.type && item.type === 'phrasal' ? ' [phrasal]' : ''
      // textList += item['word'] + score + typeLabel + '\n'
      textList += item['word'] + '\n'
    }
    editor2Content = textList
  }

This is how the cookies are set when I log in
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

When I try to fetch rhymes this is these are reponses I get
from backend hosted render:
INFO:     102.251.68.13:0 - "OPTIONS /api/lyric-tools/find-rhymes HTTP/1.1" 200 OK
INFO:     102.251.68.13:0 - "POST /api/lyric-tools/find-rhymes HTTP/1.1" 422 Unprocessable Content

from frontend in the browser:
5IFykFci.js:1 
 POST https://m-prosody.onrender.com/api/lyric-tools/save-writing-seconds 422 (Unprocessable Content)
13.CRr-bj_h.js:1 Failed to save writing seconds {"detail":[{"type":"missing","loc":["cookie","access_token"],"msg":"Field required","input":null}]}

5IFykFci.js:1 
 POST https://m-prosody.onrender.com/api/lyric-tools/save-writing-seconds 422 (Unprocessable Content)
13.CRr-bj_h.js:1 Failed to save writing seconds {"detail":[{"type":"missing","loc":["cookie","access_token"],"msg":"Field required","input":null}]}


When I check the cookies are saved in the browser
Here is how I set my CORS in my main.py:
origins = [
    "*"
    "http://localhost:5173",
    "https://m-prosody.vercel.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
