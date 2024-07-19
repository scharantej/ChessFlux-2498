## Flask Application Design for a Simple Chess App

### HTML Files

- **index.html**: The main landing page of the application. Will contain the game board and controls.
- **stylesheet.css**: Contains styling for the application, including the chess board and pieces.
- **scripts.js**: Contains JavaScript code for handling user interactions, such as moving pieces and checking for check/checkmate.

### Routes

- **home**: The main route, which renders the `index.html` page.
- **move**: An API route that handles a user's move. It checks if the move is valid and updates the game state accordingly.
- **check**: An API route that checks if the current player is in check or checkmate.
- **reset**: A route that resets the game to its initial state.