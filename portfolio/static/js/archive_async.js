// Handle the async archived company result calls to django backend
function reload_archived_companies(number) {
    $.ajax(
        {
            type: "GET",
            url: filter_companies_url,
            data: {
                filter_number: number
            },
            success: function (data) {
                $(".companies-table").html(data);
            }
        })
}

// Handle the async archived individual result calls to django backend
function reload_archived_individuals(number) {
    $.ajax(
        {
            type: "GET",
            url: filter_individuals_url,
            data: {
                filter_number: number
            },
            success: function (data) {
                $(".individuals-table").html(data);
            }
        })
}