

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
			  type: "POST",
			  url: "/api/upload",
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
					'<div class="alert alert-info"><i class="fa fa-exclamation-triangle"></i> Extension not good only try with <strong>GIF, JPG, PNG, JPEG</strong>.</div>'
				  );

				  $("#result_traits").html(data);

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


/*$(document).ready( function() {
    	$(document).on('change', '.btn-file :file', function() {
		var input = $(this),
			label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
		input.trigger('fileselect', [label]);
		});

		$('.btn-file :file').on('fileselect', function(event, label) {
		    
		    var input = $(this).parents('.input-group').find(':text'),
		        log = label;
		    
		    if( input.length ) {
		        input.val(log);
		    } else {
		        if( log ) alert(log);
		    }
	    
		});
		function readURL(input) {
		    if (input.files && input.files[0]) {
		        var reader = new FileReader();
		        
		        reader.onload = function (e) {
		            $('#img-upload').attr('src', e.target.result);
		        }
		        
		        reader.readAsDataURL(input.files[0]);
		    }
		}

		$("#imgInp").change(function(){
		    readURL(this);
		}); 	
	});

    */