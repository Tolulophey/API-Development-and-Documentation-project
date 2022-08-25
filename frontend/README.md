# Frontend - Trivia API

## Getting Setup

This frontend is designed to work with [Flask-based Backend](../backend) so it will not load successfully if the backend is not working or not connected.

### Installing Dependencies

1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```
npm install
```

## Starting App
To start the app in order to play game or just explore the App, open your terminal, navigate to the frontend directory and run the code
```
npm start
```

## Game Play Mechanics
### General
All questions are listed under the list tab where the user has the ability to view the questions and show answer to the question. You can choose to choose the your category of interest to view the questions available as well and search a particular question.

### Adding new question
A new question can be added via the Add tab by filling the available form with your question, corresponding answer, difficulty level and category. The question will be added upon successful form submission. You can verify your question in the List tab either by checking for the question umder the selected category or by searching for it directly in the search box

### Playing the game
When a user plays the game, they play up to five questions of the chosen category. If there are fewer than five questions in a category, the game will end when there are no more questions in that category.

Random questions will be generated out of the questions available under the category, the Player inputs answer and submit and the answer to the question asked will be displayed and the player will be able to know whether or not he got the question write or wrrong
