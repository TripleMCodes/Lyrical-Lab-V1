import logging
import requests
from pathlib import Path
import sys
logging.basicConfig(level=logging.DEBUG)

API_KEY = Path(__file__).parent / "secrets" / ".env"

if not API_KEY.exists():
    logging.debug("API key not found")
    sys.exit()

class OpenRouterClient:
    def __init__(self, model="meta-llama/llama-3-70b-instruct", app_title="Autodidex", referer="https://Autodidex.com"):
        self.api_key = API_KEY.read_text().strip()
        self.model = model
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "X-Referer": referer,
            "X-Title": app_title
        }

    def _send_request(self, prompt):
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            response = requests.post(self.url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            logging.debug(f"API request failed {e}")
            return None
    
    def generate_lyrics(self, theme, genre):
        prompt = f"""Give me 3 poetic and creative song lyric ideas about '{theme}' , styled like a modern emotional {genre} song"""

        return self._send_request(prompt)
    
    def summarize_text(self, text):
        prompt = f"""Summarize the following text in bullet points: {text}"""
        return self._send_request(prompt)
    
    def cliches_phrase_quotes(self, theme, figure_of_speech):
        prompt = f"Give me a {figure_of_speech} related to {theme}"
        return self._send_request(prompt)

    def critique_lyrics(self, lyrics):
        prompt = """
                I’m going to share some lyrics. I want you to critique them the way a seasoned songwriter, poet, and music critic would. Analyze them for:

                Theme and Emotion: What feelings or story come through? Is it cohesive or scattered?

                Imagery and Metaphor: Are the images powerful, fresh, and evocative?

                Flow and Structure: Comment on rhythm, pacing, rhyme scheme, and overall musicality.

                Word Choice and Diction: Are the words vivid, too plain, or too complex for the tone?

                Authenticity: Does it feel honest, or forced? What kind of persona or voice emerges?

                Suggestions: Offer specific ideas for improvement (e.g., tightening a verse, reworking metaphors, or changing rhyme patterns).

                Keep the tone constructive but real — like a producer giving notes to an artist they believe in. Be analytical, but also interpretive and artistic. Feel free to reference literary or musical comparisons if it helps clarify your points.

                Here are the lyrics:
                """

        prompt += lyrics
        return self._send_request(prompt)
        
    
if __name__ == "__main__":
    
    or_client  = OpenRouterClient()

    logging.debug(or_client.generate_lyrics("Last time I saw you was in a dream", "Pop"))
#     logging.debug(or_client.cliches_phrase_quotes("Love", "metaphor"))
#     # logging.debug(or_client.summarize_text("The quick brown fox jumps over the lazy dog. This is a classic example of a pangram, which is a sentence that contains every letter of the alphabet at least once. Pangrams are often used to test fonts and keyboards."))