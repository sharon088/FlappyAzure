# Floopy Bird 🐦

Welcome to **Floopy Bird**, a delightful clone of the classic **Flappy Bird** game with added features like user registration, persistent leaderboards, and a fully dockerized setup. Challenge yourself to achieve the highest score while dodging pipes and competing on the leaderboard!

## 🎮 Game Features

- **Registration**: Start the game by registering or logging in.
- **Simple Controls**: Press the **space bar** to "floop" (flap) and navigate through the pipes.
- **Leaderboard**: Check the leaderboard displayed on the left to see top players and compete for the highest score.
- **Dynamic Gameplay**: Gravity, responsive controls, and obstacles keep the game exciting.

## 🚀 Getting Started

### 1. Prerequisites

- Docker installed on your system
- A running MongoDB instance for persistent leaderboards

### 2. Local Setup

#### Using the Dockerfile

1. Build the Docker image:
   bash
   docker build -t floopy-bird .
   
2. Run the container:
   bash
   docker run -p 3000:3000 floopy-bird
   
   The game will be accessible at `http://localhost:3000`.

#### With MongoDB for Persistent Leaderboards

1. Build the Docker image with a remote MongoDB connection:
   bash
   docker build -t floopy-bird --build-arg MONGO_URI="<your_mongo_uri>" .
   
2. Run the container:
   bash
   docker run -p 3000:3000 floopy-bird
   

### 3. Using `docker-compose`

A `docker-compose.yaml` file is included for quick setup with a local MongoDB database:

1. Start the services:
   bash
   docker-compose up
   
2. Access the game at `http://localhost:3000`.

## 🔧 Customization and Development

### Modify the Backend

The backend logic is implemented in `app.py`. You can:
- Customize routes for additional features
- Adjust logging configurations
- Update the database connection logic

### Enhance the Frontend

The game's visuals and logic are managed in `static/js/game.js`. Key areas to explore:
- Game mechanics: Adjust gravity, pipe speed, or bird behavior.
- UI/UX: Modify the leaderboard display or add animations.
- Sounds and Images: Replace the existing assets in the `static` folder.

### Update the Docker Configuration

The `Dockerfile` allows you to:
- Add dependencies to enhance functionality.
- Adjust the build process for specific environments.

## 📂 Project Structure

- **app.py**: Flask backend handling routes and MongoDB interactions.
- **static/**: Contains all game assets like JavaScript, CSS, and images.
- **Dockerfile**: Used to build the Floopy Bird Docker image.
- **docker-compose.yaml**: Simplifies setup with a local database.

## 🛠️ Troubleshooting

- **Game Not Loading**: Check that the Docker container is running and accessible on `http://localhost:3000`, as well as ensure MongoDB is running and the URI is correctly configured..

## 🌟 Contributing

Feel free to (not) fork the repository, (not) make changes, and (not) submit a pull request. Contributions are (not) welcome!

---

Enjoy the game, and happy flopping!

