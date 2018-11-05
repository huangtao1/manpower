var jenkins_table = $('#jenkins_table').DataTable(
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
        "pageLength": 50,
        "pagingType": "bootstrap_full_number"
    }
);
