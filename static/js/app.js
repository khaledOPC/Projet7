	let map;
function initMap() {
	map = new google.maps.Map(document.getElementById("map"), {
		center: { lat:-34.397 , lng: 150.644},
		zoom: 8,
	});
	new google.maps.Marker({
		position: { lat: -34.397, lng: 150.644 },
		map,
		title: "Hello World!",
	});
}
window.initMap = initMap;

$(document).ready(function() {
	 $('form').on('submit', function(event) {
		event.preventDefault();
		$.ajax({
			data : {  
				search: $('#search').val(),
					},
			type : 'POST',
			url : '/message'
		})
		.done(function(data) {
			console.log(data)
			console.log(data.lat, data.lng)
			var userInput = $("<p class='bubble bubble--alt'></p>").text($('#search').val());
			$('#response').append(userInput)
			var searchReponse = $("<p class='bubble'></p>").text(data.message);
			$('#response').append(searchReponse)
			// $('#response').text(data.message)
			$('#map').css('display', 'block')
			map.setCenter({lat: data.lat, lng: data.lng})
				new google.maps.Marker({
					position: {lat: data.lat, lng: data.lng},
					map,
			});
		})
		.fail(function(data) {
			var searchReponse = $("<p class='bubble'></p>").text("Il y'a eu un problème dans le serveur");
			$('#response').append(searchReponse)
		});
	});
});
