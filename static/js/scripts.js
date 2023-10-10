let selectedPiece = null;

document.addEventListener("DOMContentLoaded", function() {
    let cells = document.querySelectorAll(".chess-cell");
    cells.forEach(cell => {
        cell.addEventListener("click", handleCellClick);
    });
});

function handleCellClick(event) {
    let cell = event.currentTarget;
    let position = getCellPosition(cell);
    if (selectedPiece) {
        // Intenta mover la pieza seleccionada a la celda clicada
        movePiece(selectedPiece, position);
        selectedPiece = null;
    } else {
        // Selecciona la pieza en la celda clicada
        selectedPiece = position;
        highlightValidMoves(position);
    }
}

function getCellPosition(cell) {
    let x = cell.parentElement.rowIndex;
    let y = Array.from(cell.parentElement.children).indexOf(cell);
    return [x, y];
}

function movePiece(start, end) {
    fetch("/move", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            start: start,
            end: end
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Mueve la pieza en la interfaz
            let sourceCell = document.querySelector(`[data-row='${start[0]}'][data-col='${start[1]}']`);
            let targetCell = document.querySelector(`[data-row='${end[0]}'][data-col='${end[1]}']`);
            targetCell.innerHTML = sourceCell.innerHTML;
            sourceCell.innerHTML = "";
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

function highlightValidMoves(position) {
    // Aquí, en una implementación completa, podrías consultar al servidor 
    // para obtener los movimientos válidos y luego destacar esas celdas.
    // Para mantenerlo simple, este método no hace nada en esta versión básica.
}

