// 在游戏结束时保存分数
function ballLeaveScreen() {
    lives--;
    if (lives) {
        // 重置小球
    } else {
        saveScore(score); // 保存分数
        alert('Game Over!');
        location.reload();
    }
}
