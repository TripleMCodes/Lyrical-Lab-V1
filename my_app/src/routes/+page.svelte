<script>
      import './home.css';
      import {fetchWords} from '../lib/api/client'
      import {fetchRhymes} from '$lib/api/lyric_tools'
      import SigilSpinner from '../lib/components/SigilSpinner.svelte';
      import {get_url} from '$lib/url_vars/urls_vars'

	let isLoading = $state(false);
      let selected = $state('')
      let word = $state('')
      let wordList = $state([])
      let phraseList = $state([])
      let notify = $state('No words searhed yet')

      async function fetchWordsWrapper(){
            isLoading = true
            if (selected === "rhyme"){
                 
                  try {
			const res = await fetch(`https://m-prosody.onrender.com/api/public/get-rhymes`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ word: word })
			});

                        const data = await res.json();
                        console.log('the data is ', data)
                        console.log('the data is ', data.message)
                        wordList = data.word_rhymes;
                        phraseList = data.phrasal_rhymes;
                        console.log('the phrasal rhymes ', data.phrasal_rhymes);
                        // wordList.push(...data.phrasal_rhymes)
                        word = '';
                        isLoading = false;
                  } catch (err) {
                       const data = { error: 'Request failed' };
                  } finally {
                        isLoading = false;
		      }
                  
                  
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


<section class="hero">
      <div class="hero-image">
            <span class="phoneme-tag">ə</span>
            <span class="phoneme-tag">ʌ</span>
            <span class="phoneme-tag">ɪ</span>
            <div class="hero-image-inner">
                  <div class="waveform">
                  {#each [30, 55, 75, 90, 65, 45, 80, 50, 35, 70, 85, 40, 60, 75, 30] as h}
                  <div class="waveform-bar" style="height: {h}px;"></div>
                  {/each}
                  </div>
            </div>
      </div>



      <div class="hero-content">
            <p class="eyebrow">Welcome to M-Prosody</p>
            <h1>Write lyrics that <em>sound</em> right.</h1>
            <p>Experiment with rhymes, synonyms, homophones, and related words. Build your lyrics, check your syllables, and save your creations in your personal notebook.</p>
            <p>M-Prosody's rhyme engine doesn't look at how words are spelled — it listens to how they sound. It matches rhythm, stress, and vowel flow to find rhymes that actually feel right, then ranks them by strength.</p>
            <p class="engine-note">The engine is still evolving. For now, it understands <strong>sound</strong>, not meaning.</p>
            <a href="/lyrical-lab" class="cta-btn">Start Writing →</a>
      </div>
</section>



<section id="search" class="search-section">
      <h2>Lexical Tools</h2>
      <div class="search-box">
            <input type="text" id="word-input" placeholder="Enter search here..." bind:value={word}>
            <select id="search-type" bind:value={selected} onchange={() => console.log(selected)}>
                  <option value="rhyme">Rhyme</option>
                  <option value="synonym">Synonym</option>
                  <option value="related">Related</option>
                  <option value="homophone">Homophone</option>
            </select>
            <button id="search-btn" onclick={fetchWordsWrapper}>Find Words</button>
      </div>

      {#if isLoading}
            <SigilSpinner text="Consulting the lexicon…" />
      {:else}

      {#if wordList.length > 0}
            <ul id="results-list">
                  {#if phraseList.length > 0}
                        {#each phraseList as lst (lst.phrase)}
                              <li>{lst.phrase}</li>
                        {/each}
                  {/if}
                  {#each wordList as lst (lst.word)}
                        <li>{lst.word}</li>
                  {/each}
            </ul>
      {/if}

     

      {#if wordList.length === 0 && phraseList.length === 0}
            <div class="notify">
                  <p>{notify}</p>
            </div>
      {/if}

      {/if}

      

</section>