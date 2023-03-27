var search_input = document.getElementById('search_input');
var searchInputs = $('.search_input');
var results_container = document.getElementById('results_container');
var isClickInside = false;


// Show or Hide the table depending on if the search input is active or not
document.addEventListener('click', function (event) {
    if (searchInputs.is(event.target)) {
        isClickInside = true;
      } else {
        isClickInside = false;
      }

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
$('.search_input').keyup(function (event) {
    var resultsContainer = $(this).closest('.border').find('#results_container')[0];
    results_container = resultsContainer;
    search_input = $(this);

    $.ajax(
        {
            type: "GET",
            url: search_url,
            data: {
                searchresult: search_input.val()
            },
            success: function (data) {
                $(resultsContainer).html(data);
            }
        })
});