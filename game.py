import pandas as pd
import random
from matplotlib import pyplot as plt
import numpy as np


df = pd.read_csv("unigram_freq.csv")
# filter out words with punctuation or are short.

df = df[df['word'].str.isalpha() & (df['word'].str.len() >= 3)]

class GameManager:

    def __init__(self, mode):
        self.mode = mode
        self.lives = ["\U0001F49A"] * 3
        self.word = self.get_word().lower()
        self.revealed = ["_" for _ in self.word]
        self.guessed_letters = set()
        self.wrong_tries = 0
        self.game_over = False

    def get_word(self):
        row = random.randint(0, len(df) - 1)
        return df.iloc[row, 0]

    def attempt(self, guess):
        letter = guess.lower()
        # Replaced _ with letter if the user guesses a valid letter.

        if letter in self.word and letter not in self.guessed_letters:
            for i, char in enumerate(self.word):
                if letter == char:
                    self.revealed[i] = char
        else:
            # If the users guess is wrong the number of wrong tries is incremented
            self.wrong_tries += 1
            if (self.mode == "hard" and self.wrong_tries > 6) or \
               (self.mode == "easy" and self.wrong_tries > 9):
                self.game_over = True

        self.guessed_letters.add(letter)

    def draw_hangman(self):

        # Defines a lists of tuples that correspond to the coordinates of each component of a hangman drawing.
        steps = [
            ([0, 0], [0, 6]),
            ([0, 4], [6, 6]),
            ([4, 4], [6, 5]),
            *self.head_circle(),
            ([4, 4], [4, 3]),
            ([4, 3.5], [3, 1]),
            ([4, 4.55], [3, 1]),
            ([4, 3.5], [3.5, 3]),
            ([4, 4.5], [3.5, 3])
        ]

        # Configure grid.

        fig, ax = plt.subplots(figsize=[10,10])
        ax.set_aspect('equal')

        # Draw each component of the hangman up to the number of wrong tries.

        for i in range(min(self.wrong_tries, len(steps))):
            x, y = steps[i]
            ax.plot(x, y)

        # configure grid.
        ax.set_xlim(-1, 6)
        ax.set_ylim(0, 7)
        ax.grid(which='both', color='grey', linewidth=1, linestyle='-', alpha=0.2)
        plt.show()

        return fig

    def draw_hangman_hard(self):
        # Defines the coordinates of the hangman components, but without the gallows.
        steps = [
            *self.head_circle(),
            ([4, 4], [4, 3]),
            ([4, 3.5], [3, 1]),
            ([4, 4.55], [3, 1]),
            ([4, 3.5], [3.5, 3]),
            ([4, 4.5], [3.5, 3])
        ]
        # Configure grid
        fig, ax = plt.subplots(figsize=[10,20])
        ax.set_aspect('equal')


        # Draw gallows
        ax.plot([0, 0], [0, 6], color='black')
        ax.plot([0, 4], [6, 6], color='black')
        ax.plot([4, 4], [6, 5], color='black')

        # Draw each component of the hangman up to wrong tries.

        for i in range(min(self.wrong_tries, len(steps))):
            x, y = steps[i]
            ax.plot(x, y)

        # Configure grid settings

        ax.grid(which='both', color='grey', linewidth=1, linestyle='-', alpha=0.2)
        ax.set_xlim(-1, 6)
        ax.set_ylim(0, 7)
        plt.show()

        return fig

    def head_circle(self):

        # Defines the formula needed to draw the head.

        head_radius = 0.5
        head_centre = (4, 4.5)
        theta = np.linspace(0, 2 * np.pi, 100)
        circle_x = head_radius * np.cos(theta) + head_centre[0]
        circle_y = head_radius * np.sin(theta) + head_centre[1]
        return [(circle_x, circle_y)]
