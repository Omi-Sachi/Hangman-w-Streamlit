from game import GameManager
import streamlit as st


# The Apps header layout.

st.title("🎯 Hangman :red[Game]")
st.subheader(":Red[Rules]")
st.text("Guess the letters before the man is hanged! \nWith each incorrect guess a section of the hangman is drawn,\ncomplete the drawing and GAME OVER! ")

# Allows user to select mode
mode = st.selectbox("Choose Mode:", ["", "easy", "hard"], index=0)

# Button that starts the Game session

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

button_clicked = st.session_state.button_clicked
button_label = "Start Game ⭐" if not button_clicked else "Restart Game 🔁"

# Changes the buttons functionality when pressed.

if st.button(button_label):
    if not button_clicked:
        # First click → start game
        st.session_state.button_clicked = True
        st.session_state.game = GameManager(mode)
        st.rerun()
    else:
        # Second click → reset everything
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# To prevent Game(mode) being called without mode, block starting.
if "game" not in st.session_state:
    st.warning("Please choose a mode and start the game.")
    st.stop()

game = st.session_state.game

# Depending on mode display hangman figure.

if game.mode == "hard":
    fig = game.draw_hangman_hard()
else:
    fig = game.draw_hangman()

st.pyplot(fig)

# Display revealed letters.
cols = st.columns(len(game.revealed))
for i, char in enumerate(game.revealed):
    with cols[i]:
        st.text(char.upper())

# Allow users to input guess.

st.write(game.word)
guess = st.text_input(
    f"Enter a letter (Wrong attempts: {game.wrong_tries})",
    placeholder="Enter a letter",
    max_chars=1
)

if st.button("Enter!") and guess.isalpha():
    game.attempt(guess)
    st.rerun()

# Game over conditions.

if "".join(game.revealed).lower() == game.word.lower():
    # Display a winning message:
    st.success("You have won the game! \n Restart the game to play another round!!!")


if game.game_over:
    st.warning("Game over! The word was: {}".format(game.word))
    st.warning("Better luck next time, restart the game for another try!")

