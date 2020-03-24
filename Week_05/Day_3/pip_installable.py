"""Module Docstring"""
​
import re
​
class TextCleaner():
​
    """Class Docstring"""
​
    def __init__(self, text):
        self.text = text
​
​
    def clean_simple_text(self) -> str:
        """
           Function (outside class) / Method (within class)
​
           Takes in some text (str).
           Cleans it with regular expressions.
           Returns clean text (str).
        """
        text = re.sub('\<|\>|\.|\?|\'|\"|,|\/', " ", self.text)
        text = re.sub('\s+', " ", text)
        text = text.lower()
        clean_text = text.strip()
        return clean_text
​
    def clean_lyrics(self):
        pass
​
    def clean_scientific_text(self):
        pass
​
    def clean_spanish_text(self):
        pass
​
### Functions outside of class go here.
​
if __name__ == '__main__':
​
    #Run whatever is here if I explicitly call "python text_cleaning_module.py"
    #But DONT run whatever is here if I just say "import text_cleaning_module"
​
    TEXT = "Hello <a> </a> .? ' this IS a Song.'"
    tc = TextCleaner(TEXT)
    result = tc.clean_simple_text()
    print(result)
