<script>
      import './home.css';
      import {fetchWords} from '../lib/api/client'
      // import SigilSpinner from '$lib/components/SigilSpinner.svelte';
      import SigilSpinner from '../lib/components/SigilSpinner.svelte';

	let isLoading = $state(false);
      let selected = $state('')
      let word = $state('')
      let wordList = $state([])
      let notify = $state('No words searhed yet')

      
   
      async function fetchWordsWrapper(){
            isLoading = true
            const lst = await fetchWords(selected, word)
            wordList = lst
            console.log($state.snapshot(wordList))
            if (wordList.length === 0){
                  notify = "No results found"
            }
            word = ''
            isLoading = false
      }
</script>


<section class="intro">
      <h2>Welcome to Lyrical Lab</h2>
      <p>Experiment with rhymes, synonyms, homophones, and related words. Build your lyrics, check your syllables, and save your creations in your personal notebook.</p>
      <a href="/lyrical-lab" class="cta-btn">Start Writing</a>
</section>

<section id="search" class="search-section">
      <h2>Lyric Tools</h2>
      <div class="search-box">
            <input type="text" id="word-input" placeholder="Generate lyrics..." bind:value={word}>
            <select id="search-type" bind:value={selected} onchange={() => console.log(selected)}>
                  <option value="rhyme">Rhyme</option>
                  <!-- <option value="nearRhyme">nearRhyme</option> -->
                  <option value="synonym">Synonym</option>
                  <option value="related">Related</option>
                  <option value="homophone">Homophone</option>
                  <!-- <option value="gen-lyrics">Generate lyrics</option> -->
            </select>
            <button id="search-btn" onclick={fetchWordsWrapper}>Find Words</button>
      </div>

      {#if isLoading}
	      <SigilSpinner text="Consulting the lexicon…" />
      {/if}
      {#if wordList.length > 0}
            <ul id="results-list">
                  {#each wordList as lst (lst.word)}
                        <li>{lst.word}</li>
                  {/each}
            </ul>
      {:else if isLoading === false}
            <div class="notify">
                  <p>{notify}</p>
            </div>
      {/if}

</section>