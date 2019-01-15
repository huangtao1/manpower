$("#system_menu_table").treetable({expandable: true});

// Highlight selected row
$("#system_menu_table tbody").on("mousedown", "tr", function () {
    $(".selected").not(this).removeClass("selected");
    $(this).toggleClass("selected");
});

// Drag & Drop Example Code
$("#system_menu_table .file, #system_menu_table .folder").draggable({
    helper: "clone",
    opacity: .75,
    refreshPositions: true,
    revert: "invalid",
    revertDuration: 300,
    scroll: true
});

$("#system_menu_table .folder").each(function () {
    $(this).parents("#system_menu_table tr").droppable({
        accept: ".file, .folder",
        drop: function (e, ui) {
            var droppedEl = ui.draggable.parents("tr");
            $("#system_menu_table").treetable("move", droppedEl.data("ttId"), $(this).data("ttId"));
        },
        hoverClass: "accept",
        over: function (e, ui) {
            var droppedEl = ui.draggable.parents("tr");
            if (this != droppedEl[0] && !$(this).is(".expanded")) {
                $("#system_menu_table").treetable("expandNode", $(this).data("ttId"));
            }
        }
    });
});


function setMenuActivate(activate){
    var selected = $(".selected");
    if(selected.length){
        var menu_id = $(".selected").data().ttId;
        bootbox.confirm("Are you sure?", function(result) {
           if(result){
               $.getJSON($SCRIPT_ROOT+'/manager/_menu_activate',{
                   id: menu_id,
                   activate: activate
               }, function(data){

                   bootbox.alert("Success");
                   if (!selected.data('ttParentId')) {
                        $("#system_menu_table tr").each(function (trindex, tritem) {
                            if($(tritem).data('ttParentId') == selected.data('ttId')){
                                $($(tritem).children()[2]).text(activate);
                            }
                        });
                   }else{
                       $(selected.children()[2]).text(activate);
                   }
                   location.reload()
               });
           }
        });
    }else{
        bootbox.alert("请选择一个菜单!");
    }
}

$("#system_menu_table tr").dblclick(function(){
    window.location.href = $SCRIPT_ROOT + '/manager/edit_menu/' + $(this).attr('data-tt-id');
});