$(document).ready(function() {
    var daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    var today = new Date();
    var dayOfWeek = today.getDay();
    var formattedDate = today.toLocaleDateString();

    $("#todays-date").text(formattedDate);
    $("#day-of-week").text(daysOfWeek[dayOfWeek]);
});

function updateDueDate(taskId, dueDate) {
    var taskElement = $("#" + taskId + " .task-details");
    var taskName = taskElement.find(".task-name").text().trim();

    $.post("/edit/" + taskId, { task: taskName, due_date: dueDate }, function(data) {
        // Update the UI here instead of reloading the page
    });
}

window.editTask = function(taskId) {
    var taskNameElement = $("#" + taskId + " .task-details .task-name");
    var taskName = taskNameElement.text().trim();
    var newTaskName = prompt("Enter the new task name:", taskName);

    if (newTaskName !== null && newTaskName.trim() !== "") {
        // Perform task editing logic
        taskNameElement.text(newTaskName);

        // Send AJAX request to update the task name on the server-side
        $.post("/edit/" + taskId, { task: newTaskName }, function(data) {
            // Reload the page after a short delay
            setTimeout(function() {
                location.reload();
            }, 1500);
        });
    }
};

$(".sortable").sortable({
    handle: ".drag-handle",
    update: function(event, ui) {
        var taskIds = $(this).sortable("toArray");
        $.post("/rearrange", { taskIds: taskIds });
    }
}).disableSelection();

$("#clear-completed").click(function() {
    $.post("/clear-completed", function(data) {
        location.reload();
    });
});

function updateDueDate(taskId, dueDate) {
    var taskElement = $("#" + taskId + " .task-details");
    var taskName = taskElement.find(".task-name").text().trim();

    $.post("/edit/" + taskId, { task: taskName, due_date: dueDate }, function(data) {
        location.reload();
    });
}

