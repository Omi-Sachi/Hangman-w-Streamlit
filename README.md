# HangMan Using streamlit

![Game StartPage](https://raw.githubusercontent.com/Omi-Sachi/Hangman-w-Streamlit/main/images/Startgame.png)

This project was an oppurtunity for me to learn a popular framework called streamlit that allows you to deploy web applications with minimal code ( or so they say).

In this project I created a Hangman game that randomly selects a word from a word bank, and allows the user to guess a letter. The aim of the game, is to guess the word within
a certain number of guess defines by the components in the hangman drawing e.g the arms, legs and head.

To draw the hangman over a cartesian plane and have it "dynamically" develop with each mistake I used matplotlib, this was honestly one of my favourite parts of the projects.
I kept wondering how I was going to display the hangman and the it clicked, streamlit works so well with graphs and libraries like matplotlib making connecting them seamless,

## My biggest challenges

### Re-runs:

I can’t fully describe how challenging the reruns in Streamlit have been for my projects. For those who don’t know:

Streamlit runs your entire Python script from top to bottom every time something in the app’s state changes. This can happen when a user presses a button, switches tabs, or interacts with any widget.
The problem I kept encountering involved buttons that take user input for example, a guess in a game and should immediately update the UI if the guess is wrong. But because Streamlit reruns the whole script each time, 
the button’s action only triggers during that specific run, and changes to the ui aren't made untill the button is clicked again creating a delay.

As a consequence if a user made two mistakes in a row followed by a correct guess, nothing would happen visually on the first mistake, then something would appear after the second mistake, 
and the correct guess would show that a mistake was made as it's refering to the mistake made in the turn prior.

### How I fixed this:

I used `st.session_state` to save game data, so then when I called st.rerun() which will rerun the script and the line of code responsible for the ui the app to remembers what happened during the previous run.
This way, the UI updates immediately on the same button press.

### The dynamic button
I realized that the game needed two button one to start the game, which is only needed because the whole file is read at once and we call he function Gamemager with a parameter mode
so if mode han't been selected yet an error occur so this button is a way of ensure mode has been selected.
then we neede a restart button either if the user has finished the gme and want to to rey again.
I idn't want to have two buttons on the same form instead i wanted one button whos funcion changed after you pressed.
I knew that when you prressed the button it would become true and when it's pressed again false, hus i could have a condition saying if it's true or false, change function.

to do this i used these lines of code
```python
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

button_clicked = st.session_state.button_clicked
button_label = "Start Game ⭐" if not button_clicked else "Restart Game 🔁"

```
The code above stores the boolean value of button clicked in the session state so that it isn't written over in every rerun as the user interact with the program.
I then changed the button lable using a condition : If button clicked is false it hasn't been clicked and should be start game, if it has been clicked that it's true, 
it's lable becomes restart game.

```python
if st.button(button_label):
    if not button_clicked:
        # First click  start game
        st.session_state.button_clicked = True
        st.session_state.game = GameManager(mode)
        st.rerun()
    else:
        # Second click  reset everything
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
```

The first line " if st.button(button_label) " is used to identify wether the button was clicked in the current run, 
whereas the conditon underneither refers to the variable button_clicked that is stored in the games session state, the value that persist over each rerun. 
This allows us to know the state ( true or false) of the button before and after it's been clicked, which we can map onto conditons we want for the button.

### The drawing system

Figuring out how to draw the hangman with the least amount of code was difficult, I was initially going to use conditions ( if statements ) and manually write out
what needs to be drawn for each wrong guess. I knew this would take too long, so instead I implemeted a list of coordinates and used a for loop to iterate through each element in the list up to 
the number of wrong tries. I would then call ax.plot(x, y), which takes tuples.

I was hesitant using this method because I have to redraw all components again with every rerun including if the guesses are wrong, which I feel to be inefficient.
So I plan on updateing my program to include conditionals on when to redraw everything and using session states to keep track of what already drawn.


## Future updates:
### A list of improvements:
1. The database I used has alot of spelling mistakes and words that nobody would guess correctly, I want to clean the data.
2. Add a hint system, this should allow the user to engage even when they don't know the word instead of guessing randomly.
3. Create a more challenging hard mode, currently only the number of tries the user has available reduces, which isn't challenging enough.
I think meauring the difficulty level of the words would be a good way to challenge the user.



