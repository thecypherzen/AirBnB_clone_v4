// global functions
// 1. get a user
async function getUser(userId) {
    url = `http://0.0.0.0:5001/api/v1/users/${userId}`;
    response = await fetch(url, {
        headers: {"Content-Type": "application/json"}
    });
    data = await response.json();
    return(data);
}
// 2. create an article from a place object
async function createPlaceArticle(placeObj){
    const article = $("<article></article>");
    // add headline and price_by_night to headline_wrapper
    const headlineWrapper = $("<div>").addClass("headline-wrapper")
          .append($("<h2>").addClass("headline").text(`${placeObj.name}`),
                  $("<div>").addClass("price_by_night")
                  .text(`${placeObj.price_by_night}`)
                 );
    // add max_guests, num_of_rooms and num_bathrooms to information
    const information = $("<div>").addClass("information")
          .append(
              // max_guests
              $("<div>").addClass("max_guest").append(
                  $("<div>").addClass("guest_icon"),
                  $("p").text(`${placeObj.max_guest} Guests`)
              ),
              // number_rooms
              $("<div>").addClass("number_rooms").append(
                  $("<div>").addClass("bed_icon"),
                  $("p").text(`${placeObj.number_rooms} Bedroom`)
              ),
              // number_bathrooms
              $("<div>").addClass("number_bathrooms").append(
                  $("<div>").addClass("bath_icon"),
                  $("p").text(`${placeObj.number_bathrooms} Bathroom`)
              )
          );

    // create owner div
    const owner = await getUser(placeObj.user_id)
          .then(success => success)
          .catch(fail => fail);

    const ownerDiv = $("<div>").addClass("user")
          .html(`<b>Owner</b>: ${owner.first_name} ${owner.last_name}`);
    const description = $("<div>").addClass("description")
          .text(`${placeObj.description}`);
    article.append(headlineWrapper, information, ownerDiv, description);
    return article;
}

// Create places section
const placesSection = $("<section></section>").addClass("places")
      .append($("<h1>").text("Places"));


// fetch places from api
async function getAllPlaces(url){
    console.log("all places called");
    res = await fetch(url, {
        method: "POST",
        body: JSON.stringify({}),
        headers: {"Content-Type": "application/json"}
    });
    return await res.json();
}

// Entry
$("document").ready(async () => {
    // FILTER SECTION
    // add listener to input of type checkbox
    let selected = {};
    $("input:checkbox").on("change", function() {
	      let key = $(this).attr('data-id');
	      if ($(this).is(":checked")) {
	          selected[key] = $(this).attr("data-name");
	      } else {
	          delete selected[key];
	      }

	      // create is to of selected checkboxes
	      let list = "";
	      for (let value of Object.values(selected)) {
	          if (list.length) {
		            list += ", ";
	          }
	          list += value;
	      }

	      // append selected checkboxes to h4
	      $("div.amenities h4").html(`<p>${list}</p>`);
    });

    // SERVER STATUS
    // Update server status
    const apiBadge = $("#api_status");
    let url = "http://0.0.0.0:5001/api/v1/status/";
    $.get(url, (res, xhrObj) => {
	      apiBadge.addClass("available");
    }).fail(err => {
	      console.log(err);
	      apiBadge.removeClass("available");
    });

    // UPDATE PLACES FROM UI
    url = "http://0.0.0.0:5001/api/v1/places_search/";
    const allPlaces = await getAllPlaces(url);
    console.log(allPlaces);
});
