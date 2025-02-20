import * as bootstrap from 'bootstrap';

document.getElementById('tournament-selector').addEventListener('change', function() {
    var tournamentId = this.value;
    if (tournamentId) {
        fetch(`/api/tournament/${tournamentId}`)
            .then(response => response.json())
            .then(data => {
                var tournamentInfo = document.getElementById('tournament-info');
                var upcomingGamesList = document.getElementById('upcoming-games-list');
                var participantsList = document.getElementById('participants-list');

                upcomingGamesList.innerHTML = '';
                participantsList.innerHTML = '';

                data.upcoming_games.forEach(game => {
                    var li = document.createElement('li');
                    li.className = 'd-flex gap-1';
                    li.innerHTML = `<div class="game-name">${game.game_name}</div> <div class="game-time">${game.game_time}</div>`;
                    upcomingGamesList.appendChild(li);
                });

                data.participants.forEach(user => {
                    var li = document.createElement('li');
                    li.className = 'd-flex';
                    li.innerHTML = `<div class="username">${user.username}</div> <div class="email">${user.email}</div>`;
                    participantsList.appendChild(li);
                });

                tournamentInfo.style.display = 'block';
            });
    } else {
        document.getElementById('tournament-info').style.display = 'none';
    }
});
