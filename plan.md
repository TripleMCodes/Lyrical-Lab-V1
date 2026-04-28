Can you optimize this for me, I need part that display phrasal rhyme to display it conditional.


<script>
...

 async function fetchWordsWrapper(){
            isLoading = true
            if (selected === "rhyme"){
                  const data = await fetchRhymes(word)
                  console.log('the data is ', data)
                  console.log('the data is ', data.message)
                  wordList = data.word_rhymes;
                  phraseList = data.phrasal_rhymes;
                  console.log('the phrasal rhymes ', data.phrasal_rhymes);
                  // wordList.push(...data.phrasal_rhymes)
                  word = '';
                  isLoading = false;
            }
            else{
                  const lst = await fetchWords(selected, word);
                  wordList = lst;
                  // console.log($state.snapshot(wordList))
                  if (wordList.length === 0){
                        notify = "No results found"
                  }
                  word = ''
                  isLoading = false
            }
      }
</script>

{#if isLoading}
	      <SigilSpinner text="Consulting the lexicon…" />
      {/if}
      {#if wordList.length > 0}
            <ul id="results-list">
                  {#each wordList as lst (lst.word)}
                        <li>{lst.word}</li>
                  {/each}
            </ul>
            {#if phraseList.length > 0}
                  <ul id="results-list">
                        {#each phraseList as lst (lst.phrase)}
                              <li>{lst.phrase}</li>
                        {/each}
                  </ul>
            {/if}
      {:else if isLoading === false}
            <div class="notify">
                  <p>{notify}</p>
            </div>
{/if}