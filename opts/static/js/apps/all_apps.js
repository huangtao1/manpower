var apps_table = $('#apps_table').DataTable(
    {
        "language": {
            "aria": {
                "sortAscending": ": activate to sort column ascending",
                "sortDescending": ": activate to sort column descending"
            },
            "emptyTable": "No data available in table",
            "info": "Showing _START_ to _END_ of _TOTAL_ records",
            "infoEmpty": "No records found",
            "infoFiltered": "(filtered1 from _MAX_ total records)",
            "lengthMenu": "Show _MENU_ records",
            "search": "Search:",
            "zeroRecords": "No matching records found",
            "paginate": {
                "previous": "Prev",
                "next": "Next",
                "last": "Last",
                "first": "First"
            }
        },
        "bFilter": true,
        "lengthMenu": [
            [10, 50, 200],
            [10, 50, 200] // change per page values here
        ],
        // set the initial value
        "pageLength": 10,
        "pagingType": "bootstrap_full_number"
    }
);
$("#apps_table tbody").on('dblclick', 'tr', function () {
    window.location.href = $SCRIPT_ROOT + '/apps/edit_app/' + $(this).attr('data');
});
// 自定义移除从列表中移除value值
Array.prototype.removeByValue = function (val) {
    for (var i = 0; i < this.length; i++) {
        if (this[i] == val) {
            this.splice(i, 1);
            break;
        }
    }
};
var app_ids = new Array();
// 行选择
$('#apps_table tbody').on('change', 'input[type="checkbox"]', function () {
    if ($(this).parent().attr('class') == 'checked') {
        $(this).parent().removeClass("checked");
        app_ids.removeByValue($($($($(this).parent()).parent()).parent()).parent().attr('data'));
    } else {
        $(this).parent().addClass("checked");
        app_ids.push($($($($(this).parent()).parent()).parent()).parent().attr('data'));
    }
});

function stop_dev_app() {
    if (app_ids.length == 0) {
        bootbox.alert('请选择一个应用!');
    }
    else {
        $.ajax({
            url: '/apps/stop_apps',
            method: 'POST',
            data: {'app_ids': app_ids.join(',')},
            success: function () {
                window.location.reload()
            }
        });
    }
}