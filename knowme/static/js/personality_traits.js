$(document).on("click", ".browse", function() {
	var file = $(this)
	.parent()
	.parent()
	.parent()
	.find(".file");
	file.trigger("click");
});
$('input[type="file"]').change(function(e) {
	var fileName = e.target.files[0].name;
	$("#file").val(fileName);

	var reader = new FileReader();
	reader.onload = function(e) {
	// get loaded data and render thumbnail.
	document.getElementById("preview").src = e.target.result;
	};
	// read the image file as a data URL.
	reader.readAsDataURL(this.files[0]);
});

$(document).ready(function(e) {
	$("#image-form").on("submit", function() {
	$("#msg").html('<div class="alert alert-info"><i class="fa fa-spin fa-spinner"></i> Please wait...!</div>');
	$.ajax({
		//   type: "POST",
		//   url: "/api/upload",
		type: "POST",
		url: "/api/getPersonalityTraits",
		data: new FormData(this), // Data sent to server, a set of key/value pairs (i.e. form fields and values)
		contentType: false, // The content type used when sending data to the server.
		cache: false, // To unable request pages to be cached
		processData: false, // To send DOMDocument or non processed data file it is set to false
		success: function(data) {
		if (data == 1 || parseInt(data) == 1) {
			
			$("#msg").html(
			'<div class="alert alert-success"><i class="fa fa-thumbs-up"></i> Data updated successfully.</div>'
			);
		} else {
			console.log("Predictaed value is" + data)
			$("#msg").html(
			'<div class="alert alert-success">Personality Traits evaluated  successfully.</div>'
			);
		
			var Emotional_Stability = data["Emotional_Stability"]
			var Mental_Power = data["Mental_Power"]
			var Modesty = data["Modesty"]
			var Discipline = data["Discipline"]
			var Concentration = data["Concentration"]
			var Social_Isolation = data["Social_Isolation"]
			$("#result_traits").html(
				'<table border=1 class="table table-striped"> \
					<thead><tr> <th style="width:130px"> Personality Trait </th> <th style="width:130px"> Value </th> </tr> </thead> \
					<tbody> \
						<tr> <td> Emotional Stability </td> <td>' + Emotional_Stability + '</td> </tr> \
						<tr> <td> Mental Power </td> <td>' + Mental_Power + ' </td> </tr>    \
						<tr> <td> Modesty </td> <td>' + Modesty + ' </td> </tr>    \
						<tr> <td> Discipline </td> <td>' + Discipline + ' </td> </tr>    \
						<tr> <td> Concentration </td> <td>' + Concentration + ' </td> </tr>    \
						<tr> <td> Social Isolation </td> <td>' + Social_Isolation + ' </td> </tr>    \
					<tbody> \
				</table>'
				);
		}
		},
		error: function(data) {
		$("#msg").html(
			'<div class="alert alert-danger"><i class="fa fa-exclamation-triangle"></i> There is some thing wrong.</div>'
		);
		}
	});
	});
});