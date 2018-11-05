$("#organize_table").treetable({expandable: true});

// Highlight selected row
$("#organize_table tbody").on("mousedown", "tr", function () {
    $(".selected").not(this).removeClass("selected");
    $(this).toggleClass("selected");
});

// Drag & Drop Example Code
$("#organize_table .file, #organize_table .folder").draggable({
    helper: "clone",
    opacity: .75,
    refreshPositions: true,
    revert: "invalid",
    revertDuration: 300,
    scroll: true
});

$("#organize_table .folder").each(function () {
    $(this).parents("#organize_table tr").droppable({
        accept: ".file, .folder",
        drop: function (e, ui) {
            var droppedEl = ui.draggable.parents("tr");
            $("#organize_table").treetable("move", droppedEl.data("ttId"), $(this).data("ttId"));
        },
        hoverClass: "accept",
        over: function (e, ui) {
            var droppedEl = ui.draggable.parents("tr");
            if (this != droppedEl[0] && !$(this).is(".expanded")) {
                $("#organize_table").treetable("expandNode", $(this).data("ttId"));
            }
        }
    });
});


$("#organize_table tr").dblclick(function(){
    window.location.href = $SCRIPT_ROOT + '/manager/edit_organize/' + $(this).attr('data-tt-id');
});