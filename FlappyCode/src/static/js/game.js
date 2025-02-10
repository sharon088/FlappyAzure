const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d', { alpha: false });
const username = localStorage.getItem('username');
document.getElementById('display-username').textContent = username;

fetch('/leaderboard')
.then(response => response.json())
.then(data => {
    const leaderboard = document.getElementById('leaderboard');
    leaderboard.innerHTML = data.map((entry, index) => 
        `<li>${index + 1}. ${entry.username} - ${entry.score}</li>`).join('');
})
.catch(error => {
    console.error('Error fetching leaderboard:', error);
});

const DESIGN_WIDTH = 720;
const DESIGN_HEIGHT = 1000;
let BOARD_WIDTH, BOARD_HEIGHT;
const PIPE_WIDTH = 96, PIPE_HEIGHT = 768;
const BIRD_WIDTH = 51, BIRD_HEIGHT = 36;
const GRAVITY = 0.4, PIPE_SPEED = 4;

let bird = { x: 0, y: 0, velocity: 0, angle: 0 };
let pipes = [];
let score = 0, gameOver = false, pipeTimer = 0;
let isGameStarted = false; // Tracks whether the game has started

let lastTime = 0;
const FRAME_DURATION = 1000 / 60; 

const flapSound = new Audio('/sounds/sfx_wing.mp3');
const scoreSound = new Audio('/sounds/sfx_point.mp3');
const hitSound = new Audio('/sounds/sfx_hit.mp3');

const backgroundImg = new Image();
backgroundImg.src = '/images/dark-flappybirdbg.png';
const birdImg = new Image();
birdImg.src = '/images/flappybird.png';
const topPipeImg = new Image();
topPipeImg.src = '/images/dark-toppipe.png';
const bottomPipeImg = new Image();
bottomPipeImg.src = '/images/dark-bottompipe.png';

function setupSounds() {
    flapSound.volume = 0.3;
    scoreSound.volume = 0.4;
    hitSound.volume = 0.5;
}

function resizeCanvas() {
    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;

    const scaleX = windowWidth / DESIGN_WIDTH;
    const scaleY = windowHeight / DESIGN_HEIGHT;

    const scale = Math.min(scaleX, scaleY);

    const pixelRatio = window.devicePixelRatio || 1;
    canvas.width = DESIGN_WIDTH * scale * pixelRatio;
    canvas.height = DESIGN_HEIGHT * scale * pixelRatio;
    canvas.style.width = `${DESIGN_WIDTH * scale}px`;
    canvas.style.height = `${DESIGN_HEIGHT * scale}px`;

    ctx.scale(scale * pixelRatio, scale * pixelRatio);

    BOARD_WIDTH = canvas.width / (scale * pixelRatio);
    BOARD_HEIGHT = canvas.height / (scale * pixelRatio);

    bird.x = BOARD_WIDTH / 8;
    bird.y = BOARD_HEIGHT / 2;
}

function resetGame() {
    bird.y = BOARD_HEIGHT / 2;
    bird.velocity = 0;
    bird.angle = 0;
    pipes = [];
    score = 0;
    gameOver = false;
    isGameStarted = false; // Reset game state
}

function spawnPipes() {
    const gap = BOARD_HEIGHT / 5;
    const topPipeY = -PIPE_HEIGHT / 4 - Math.random() * (PIPE_HEIGHT / 2);
    pipes.push({ x: BOARD_WIDTH, y: topPipeY, passed: false, type: 'top' });
    pipes.push({ x: BOARD_WIDTH, y: topPipeY + PIPE_HEIGHT + gap, type: 'bottom' });
}

function detectCollision(bird, pipe) {
    return (
        bird.x < pipe.x + PIPE_WIDTH &&
        bird.x + BIRD_WIDTH > pipe.x &&
        bird.y < pipe.y + PIPE_HEIGHT &&
        bird.y + BIRD_HEIGHT > pipe.y
    );
}

function update(deltaTime) {
    if (!isGameStarted) return; 

    if (!gameOver) {
        bird.velocity += GRAVITY * (deltaTime / FRAME_DURATION);
        bird.y += bird.velocity * (deltaTime / FRAME_DURATION);

        bird.angle = Math.min(Math.max(bird.velocity * 3, -45), 90);

        if (bird.y > BOARD_HEIGHT) {
            gameOver = true;
            hitSound.play();
            submitScore();

        }

        pipeTimer++;
        if (pipeTimer > 70) {
            spawnPipes();
            pipeTimer = 0;
        }

        pipes = pipes.map(pipe => {
            pipe.x -= PIPE_SPEED * (deltaTime / FRAME_DURATION);

            if (!pipe.passed && bird.x > pipe.x + PIPE_WIDTH) {
                score += 0.5;
                pipe.passed = true;
                scoreSound.play();
            }

            if (detectCollision(bird, pipe)) {
                gameOver = true;
                hitSound.play();
                submitScore();
            }

            return pipe;
        }).filter(pipe => pipe.x > -PIPE_WIDTH);
    } else {
        document.getElementById('final-score').textContent = Math.floor(score);
    }
}

function draw() {
    ctx.drawImage(backgroundImg, 0, 0, BOARD_WIDTH, BOARD_HEIGHT);

    pipes.forEach(pipe => {
        ctx.drawImage(pipe.type === 'top' ? topPipeImg : bottomPipeImg, pipe.x, pipe.y, PIPE_WIDTH, PIPE_HEIGHT);
    });

    ctx.save();
    ctx.translate(bird.x + BIRD_WIDTH / 2, bird.y + BIRD_HEIGHT / 2);
    ctx.rotate(bird.angle * Math.PI / 180);
    ctx.drawImage(birdImg, -BIRD_WIDTH / 2, -BIRD_HEIGHT / 2, BIRD_WIDTH, BIRD_HEIGHT);
    ctx.restore();

    ctx.fillStyle = 'white';
    ctx.font = '45px Courier';
    ctx.fillText(`Score: ${Math.floor(score)}`, 10, 50);
}

function gameLoop(timestamp) {
    const deltaTime = timestamp - lastTime;
    lastTime = timestamp;

    if (!isGameStarted) {
        // Draw initial screen with bird and "Press Space to Start" message
        ctx.drawImage(backgroundImg, 0, 0, BOARD_WIDTH, BOARD_HEIGHT);

        ctx.save();
        ctx.translate(bird.x + BIRD_WIDTH / 2, bird.y + BIRD_HEIGHT / 2);
        ctx.drawImage(birdImg, -BIRD_WIDTH / 2, -BIRD_HEIGHT / 2, BIRD_WIDTH, BIRD_HEIGHT);
        ctx.restore();

        ctx.fillStyle = 'white';
        ctx.font = '45px Courier';
        ctx.fillText("Press Space to Start", BOARD_WIDTH / 4, BOARD_HEIGHT / 2);
    } else {
        update(deltaTime);
        draw();
    }

    requestAnimationFrame(gameLoop);
}

function submitScore() {
    fetch('/submit-score', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ score })
    })
    .then(response => response.json())
    .then(data => {
        setTimeout(() => {
            console.log('After 2 seconds');
            resetGame();
            location.reload();

        }, 2200); 
        
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error saving score. Please try again.');
    });
}

function logout() {
    fetch('/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(() => {
        window.location.href = '/login'; 
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

document.addEventListener('keydown', e => {
    if (e.code === 'Space') {
        if (!isGameStarted) {
            isGameStarted = true; 
        } else if (!gameOver) {
            bird.velocity = -7; 
            flapSound.currentTime = 0;
            flapSound.play();
        }
    }

    if (e.code === 'ControlLeft' && gameOver) {
        resetGame();
    }
});

window.addEventListener('resize', resizeCanvas);
resizeCanvas();
setupSounds(); 
requestAnimationFrame(gameLoop);
