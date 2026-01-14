import pronouncing 
import pyphen

dic = pyphen.Pyphen(lang='en')

class SyllableCounter:

    def __init__(self):
        pass
    
    def count_syllables_in_text(self, lst):
        """takes a list with lines, for each line count the syllables."""
        for line in lst:
            syllable_counts_per_line = [self.line_splitter(line) for line in lst]
            return syllable_counts_per_line
        

    def line_splitter(self, line):
        """Split a line into words and count syllables for each word. Return a list with line and number of syllbles in a line"""
        words = line.split()
        syllable_counts = [self.count_syllables(word) for word in words]
        syllable_sum = sum(syllable_counts)
        line = [line, syllable_sum]
        return line

    @staticmethod
    def count_syllables(word):
        """Count the number of syllables in a word using the pronouncing library.
        If the word is not found in the pronouncing dictionary, use pyphen as a fallback.
        """
        counter = 0

        phones = pronouncing.phones_for_word(word.lower())
        if phones:
            # Get the first pronunciation and count the syllables
            syllable_count = pronouncing.syllable_count(phones[0])
            counter += syllable_count
            return counter
        else:
            # Fallback to pyphen if the word is not found in pronouncing
            hyphenated = dic.inserted(word)
            return max(1, hyphenated.count('-') + 1)  # Ensure at least 1 syllable

lst = [
    "Fear not for I am here",
    "I am Allmight",
    "I will always be by your side",
    "I am lala paluza"
]

syllable_counter = SyllableCounter()
result = syllable_counter.count_syllables_in_text(lst)
print(result)