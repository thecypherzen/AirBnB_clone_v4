// global variables
let checkedAmenities = {}
let checkedLocations = {}
let checkdStates = {}

// global functions
// get a user from user_id
async function getUser (userId) {
    const url = `http://0.0.0.0:5001/api/v1/users/${userId}`;
    const response = await fetch(url, {
        headers: { 'Content-Type': 'application/json' }
    });
    const data = await response.json();
    return (data);
}


// fetch places from api (and filter)
async function getPlaces(url, amenities=null) {
    const res = await fetch(url, {
        method: 'POST',
        body: ! amenities ? JSON.stringify({}) :
            JSON.stringify({"amenities": amenities}),
        headers: { 'Content-Type': 'application/json' }
    });
    return await res.json();
}


// create an article from a place object
async function createPlaceArticle (placeObj) {
  const article = $('<article></article>');
  // add headline and price_by_night to headline_wrapper
  const headlineWrapper = $('<div>').addClass('headline-wrapper')
    .append($('<h2>').addClass('headline').text(`${placeObj.name}`),
      $('<div>').addClass('price_by_night')
        .text(`${placeObj.price_by_night}`)
    );
    // add max_guests, num_of_rooms and num_bathrooms to information
  const information = $('<div>').addClass('information')
    .append(
      // max_guests
      $('<div>').addClass('max_guest').append(
        $('<div>').addClass('guest_icon'),
        $('<p>').text(`${placeObj.max_guest} Guests`)
      ),
      // number_rooms
      $('<div>').addClass('number_rooms').append(
        $('<div>').addClass('bed_icon'),
        $('<p>').text(`${placeObj.number_rooms} Bedroom`)
      ),
      // number_bathrooms
      $('<div>').addClass('number_bathrooms').append(
        $('<div>').addClass('bath_icon'),
        $('<p>').text(`${placeObj.number_bathrooms} Bathroom`)
      )
    );
  // create owner div
  const owner = await getUser(placeObj.user_id)
    .then(success => success)
    .catch(fail => fail);
  const ownerDiv = $('<div>').addClass('user')
    .html(`<b>Owner</b>: ${owner.first_name} ${owner.last_name}`);
  const description = $('<div>').addClass('description')
    .html(`${placeObj.description}`);
  article.append(headlineWrapper, information, ownerDiv, description);
  return article;
}

// create places section
async function createPlacesSection(amenities=null) {
    const placesSection = $('<section></section>').addClass('places')
          .html($('<h1>').text('Places'));
    const allPlaces = await getPlaces('http://0.0.0.0:5001/api/v1/places_search/',
                                      amenities);
    const sortedPlaces = allPlaces.sort(sp => {
        return sp.name;
    });
    for (const place of sortedPlaces) {
        const placeArticle = await createPlaceArticle(place);
        placesSection.append(placeArticle);
    }
    $('div.content').html(placesSection);
}


// Entry
$(document).ready(() => {
  // FILTER SECTION HANDLER
  // add listener to input of type checkbox
  const selected = {};
  $('input:checkbox').on('change', function () {
      const liElem = $(this);
      const liParent = liElem.parent().parent().parent();
      if(liParent.is("div.amenities")){
          console.log("Amenity item:", liElem);
      } else {
          console.log("Location: ", liElem);
      }
 /*   const key = $(this).attr('data-id');
    if ($(this).is(':checked')) {
      selected[key] = $(this).attr('data-name');
    } else {
      delete selected[key];
    }

    // create is to of selected checkboxes
    let list = '';
    for (const value of Object.values(selected)) {
      if (list.length) {
        list += ', ';
      }
      list += value;
    }

    // append selected checkboxes to h4
    $('div.amenities h4').html(`${list}`); */
  });

  // CHECK INPUT IF LI IS CLICKED
    $(".popover li").on("click", function (e){
        if(! $(e.target).is("input")){
            if(! $(this).parent().is("ul.popover") ||
               $(this).parent().parent().is("div.amenities")){
                $($(this).children("input")[0]).click();
            }
        }
    });

  // SERVER STATUS
  // Update server status
  const apiBadge = $('#api_status');
  const url = 'http://0.0.0.0:5001/api/v1/status/';
  $.get(url, (res, xhrObj) => {
    apiBadge.addClass('available');
  }).fail(err => {
    console.log(err);
    apiBadge.removeClass('available');
  });

  // UPDATE PLACES FROM UI
  createPlacesSection();

  // BUTTON CLICK EVENT HANDLER - FILTERS
    $("button").on("click", (e) => {
        const selectedAmenities = Array.from($(".filters").children(".amenities")
                                         .children(".popover").children("li"))
              .filter((listItem) => {
                  return $(listItem).children("input").is(":checked");
              }).map(activeItem => {
                  return $(activeItem).children("input").attr("data-id");
              });
        createPlacesSection(selectedAmenities);
        e.preventDefault();
    });

});
