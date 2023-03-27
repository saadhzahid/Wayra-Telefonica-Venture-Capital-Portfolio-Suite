var search_input = document.getElementById('search_input');
var results_container = document.getElementById('results_container');

// Show or Hide the table depending on if the search input is active or not
document.addEventListener('click', function (event) {
    var isClickInside = search_input.contains(event.target);
    if (isClickInside) {
        //Show the search results container
        if (results_container.style.display === "none") {
            results_container.style.display = "block";
        }
    } else {
        // hide the search results container
        if (results_container.style.display === "block") {
            results_container.style.display = "none";
        }
    }
});

// Handle the async search result calls to django backend
$('.search_input').keyup(function () {
    var search_input = document.getElementById("search_input");
    console.log("called");
    $.ajax(
        {
            type: "GET",
            url: "/programme_page/search_result",
            data: {
                searchresult: search_input.value
            },
            success: function (data) {
                $('#results_container').html(data);
            }
        })
});