import string

class Tokenizer:
    """
    A class to tokenize words into numerical representations.

    The `Tokenizer` class converts words into tokens, where each character
    in the word is represented by a set of three floating-point values. These
    values capture various aspects of the character, such as its ASCII value,
    its position in the word, and a context-based influence relative to a common
    letter (e.g., 'E').

    Attributes:
    -----------
    token_length : int
        The length to which all words are normalized (default is 20).
    float_components : int
        The number of floating-point values generated for each character in the token.
    """

    def __init__(self):
        """
        Initializes the Tokenizer with default settings.

        The tokenizer is initialized with a default token length of 20 characters
        and three float components for each character.
        """
        self.token_length = 20
        self.float_components = 3

    def tokenize(self, word):
        """
        Converts a word into a token, represented by a list of tuples.

        Each character in the word is converted into a tuple of three floating-point
        values that represent various properties of the character.

        Parameters:
        -----------
        word : str
            The word to be tokenized.

        Returns:
        --------
        token : list of tuple of float
            A list where each tuple contains three floats representing a character in the word.
        """
        # Kürzen oder auffüllen, um die richtige Länge zu erreichen
        word = self.prepare_word(word)

        # Erzeuge den Token
        token = []
        for char in word:
            floats = self.char_to_floats(char, word)
            token.append(floats)

        return token

    def prepare_word(self, word):
        """
        Adjusts the word to ensure it meets the required token length.

        If the word is longer than the token length, it is truncated. If it is shorter,
        it is padded with a common letter (e.g., 'X').

        Parameters:
        -----------
        word : str
            The original word to be prepared.

        Returns:
        --------
        str
            The prepared word, truncated or padded to the required length.
        """
        # Konvertiere das Wort zu einer Länge von 20 Zeichen
        if len(word) > self.token_length:
            # Kürze das Wort
            return word[:self.token_length]
        else:
            # Fülle das Wort auf mit einem häufigen Buchstaben, z.B. 'X'
            filler = 'X' * (self.token_length - len(word))
            return word + filler

    def char_to_floats(self, char, word):
        """
        Converts a character into a tuple of three normalized floating-point values.

        The values represent:
        1. ASCII-based value, normalized between 0 and 1.
        2. Position-based value, representing the character's position in the word.
        3. Contextual influence, representing the ratio of the ASCII value relative to a common letter (e.g., 'E').

        Parameters:
        -----------
        char : str
            The character to be converted.
        word : str
            The word containing the character, used to calculate position-based value.

        Returns:
        --------
        tuple of float
            A tuple containing three floating-point values representing the character.
        """
        # ASCII-Basierter Wert (zwischen 0 und 1)
        ascii_value = ord(char)
        ascii_normalized = ascii_value / 255.0  # Normierung auf [0,1]

        # Positionsbasierter Wert (zwischen 0 und 1)
        position_value = word.index(char) / len(word)

        # Kontextueller Einfluss: Verhältnis des ASCII-Werts zu einem häufigen Buchstaben (z.B. 'E')
        common_letter_value = ord('E') / 255.0
        context_value = ascii_normalized / common_letter_value

        return (ascii_normalized, position_value, context_value)
