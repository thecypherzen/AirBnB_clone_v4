// global variables
const checkedAmenities = {};
const checkedCities = {};
const checkedStates = {};

// global functions
/**
 * updateLocations - updates h4 in locations filter
 * based on selected cities and states
 *
 * Returns: null
 */
function updateLocations () {
  // create stringed-list of selected states & cities
  let list = '';
  for (const value of Object.values(checkedStates)) {
    if (list.length) {
      list += ', ';
    }
    list += value;
  }
  for (const value of Object.values(checkedCities)) {
    if (list.length) {
      list += ', ';
    }
    list += value;
  }
  // append selected checkboxes to h4
  $('div.locations h4:first').text(`${list}`);
}

/**
 * updateAmenities - updates h4 in amenities filter
 * based on selected amenities
 *
 * Returns: null
 */
function updateAmenities () {
  // create stringed-list of selected states & cities
  let list = '';
  for (const value of Object.values(checkedAmenities)) {
    if (list.length) {
      list += ', ';
    }
    list += value;
  }
  // append selected checkboxes to h4
  $('div.amenities h4').text(`${list}`);
}

/**
 * getUser - fetches a user from api by id
 * userId: the uuid of the user to fetch
 *
 * Returns: JSONified api response data
 */
async function getUser (userId) {
  const url = `http://0.0.0.0:5001/api/v1/users/${userId}`;
  const response = await fetch(url, {
    headers: { 'Content-Type': 'application/json' }
  });
  const data = await response.json();
  return (data);
}

/**
 * getPlaces - fetch places from api, based on filters
 * (states): list of state_ids to filter results by
 * (cities): list of city_ids to filter results by
 * (amenities): list of amenities to filter results by
 *
 * Returns: Promise(resolves to JSONified api response data)
 */
async function getPlaces (url, states = null, cities = null, amenities = null) {
  const data = {};
  if (states) {
    data.states = states;
  }
  if (cities) {
    data.cities = cities;
  }
  if (amenities) {
    data.amenities = amenities;
  }
  const res = await fetch(url, {
    method: 'POST',
    body: JSON.stringify(data),
    headers: { 'Content-Type': 'application/json' }
  });
  return await res.json();
}

/**
 * createPlacesArticle - creates a single UI place <article>
 *  +based on the place's object
 *
 * (placeObj): object of place to create
 *
 * Returns: the created html <article> tag
 */
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

/**
 * createPlacesSection - creates UI places section based on elected filters
 *  +and appends it to UI
 *
 * (states): list of state_ids to filter by
 * (cities): list of city_ids to filter by
 * (amenities): list of amenity_ids to filter by
 *
 * Returns: null
 */
async function createPlacesSection (states, cities, amenities) {
  const placesSection = $('<section></section>').addClass('places')
    .html($('<h1>').text('Places'));
  const allPlaces = await getPlaces('http://0.0.0.0:5001/api/v1/places_search/',
    states, cities, amenities);
  const sortedPlaces = allPlaces.sort(sp => {
    return sp.name;
  });
  for (const place of sortedPlaces) {
    const placeArticle = await createPlaceArticle(place);
    placesSection.append(placeArticle);
  }
  $('div.content').html(placesSection);
}

/**
 * document.ready - Program entry point
 *
 * Returns: null
 */
$(document).ready(() => {
  /**
   * Filter section handler
   *
   * Updates the <h4> tag of the Locations and Amenities filters
   * +based on each check-box's checked or un-checked state
   *
   * Returns: null
   */
  $('input:checkbox').on('change', function (e) {
    if ($(this).parent().parent().is('ul.popover')) {
      const children = $(this).parent().children();
      if (children.length === 1) {
        // add or delete checked or unchecked `amenities`
        if (!$(this).is(':checked')) {
          delete checkedAmenities[$(this).attr('data-id')];
        } else {
          checkedAmenities[$(this).attr('data-id')] = $(this).attr('data-name');
        }
        updateAmenities();
      } else if (children.length === 3) {
        // add or delete checked  or unchecked `states`
        if (!$(this).is(':checked')) {
          delete checkedStates[$(this).attr('data-id')];
        } else {
          checkedStates[$(this).attr('data-id')] = $(this).attr('data-name');
        }
        updateLocations();
      }
    } else {
      // add or delete checked or unchecked `cities`
      if (!$(this).is(':checked')) {
        delete checkedCities[$(this).attr('data-id')];
      } else {
        checkedCities[$(this).attr('data-id')] = $(this).attr('data-name');
      }
      updateLocations();
    }
  });

  /**
    * delegates filters checkbox click/unclick events to
    * +their parent <li>
    */
  $('.popover li').on('click', function (e) {
    if (!$(e.target).is('input')) {
      if (!$(this).parent().is('ul.popover') ||
               $(this).parent().parent().is('div.amenities')) {
        $($(this).children('input')[0]).click();
      }
    }
  });

  /**
   * Update API Status Badge in UI
   */
  const apiBadge = $('#api_status');
  const url = 'http://0.0.0.0:5001/api/v1/status/';
  $.get(url, (res, xhrObj) => {
    apiBadge.addClass('available');
  }).fail(err => {
    console.log(err);
    apiBadge.removeClass('available');
  });

  /**
   * create UI places section
   */
  createPlacesSection();

  /**
   * Submit button click even handler
   */
  $('button').on('click', (e) => {
    createPlacesSection(Object.keys(checkedStates),
      Object.keys(checkedCities),
      Object.keys(checkedAmenities));
    e.preventDefault();
  });
});
