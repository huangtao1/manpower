var huawei_table = $('#huawei_table').DataTable(
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
$('#huawei_table tbody').on('dblclick', 'tr', function () {
    window.location.href = $SCRIPT_ROOT + '/servers/edit_hw/' + $(this).attr('data');
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
var hw_ids = new Array();
// 行选择
$('#huawei_table tbody').on('change', 'input[type="checkbox"]', function () {
    if ($(this).parent().attr('class') == 'checked') {
        $(this).parent().removeClass("checked");
        hw_ids.removeByValue($($($($(this).parent()).parent()).parent()).parent().attr('data'));
        //console.log('info:', hw_ids)
    } else {
        $(this).parent().addClass("checked");
        hw_ids.push($($($($(this).parent()).parent()).parent()).parent().attr('data'));
        //console.log('info:', hw_ids)
    }
});

function delete_hw_site() {
    if (hw_ids.length == 0) {
        bootbox.alert('请先选择一个服务器!');
    }
    else {
        bootbox.confirm('Are You Sure?', function (result) {
            if (result) {
                show_mask();
                $.ajax({
                    url: '/servers/delete_hws',
                    method: 'POST',
                    data: {'hw_ids': hw_ids.join(',')},
                    success: function () {
                        window.location.reload();
                    }
                });
            }
        });
    }
}
function copy_hw_site() {
    if (hw_ids.length == 0) {
        bootbox.alert('请先选择一个服务器!!!')
    }
    else if (hw_ids.length >1)
    {
       bootbox.alert('只能选择一个服务器!!!')
    }
    else {
        window.location.href ='/servers/copy_hwserver/'+hw_ids[0];
    }
}