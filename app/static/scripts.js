document.addEventListener('DOMContentLoaded', () => {
    const taskColumns = document.querySelectorAll('.task-column');
    taskColumns.forEach(column => {
        column.addEventListener('dragstart', handleDragStart);
        column.addEventListener('dragover', handleDragOver);
        column.addEventListener('drop', handleDrop);
    });

    function handleDragStart(event) {
        event.dataTransfer.setData('text/plain', event.target.id);
    }

    function handleDragOver(event) {
        event.preventDefault();
    }

    function handleDrop(event) {
        event.preventDefault();
        const id = event.dataTransfer.getData('text/plain');
        const draggableElement = document.getElementById(id);
        const dropzone = event.target.closest('.task-column');
        dropzone.appendChild(draggableElement);
        // Update the task status in the database using AJAX
        const taskId = id.split('-')[1];
        const newStatus = dropzone.dataset.status;
        updateTaskStatus(taskId, newStatus);
    }

    function updateTaskStatus(taskId, newStatus) {
        fetch(`/task/${taskId}/update_status`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status: newStatus }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Task status updated successfully.');
            } else {
                console.error('Error updating task status:', data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }
});
