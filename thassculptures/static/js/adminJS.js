var rh = rh || {};
rh.wp = rh.wp || {};

rh.wp.editing = false;

rh.wp.attachEventHandlers = function() {
	$("#insert-weatherpic-modal").on('shown.bs.modal', function() {
		$("input[name=image_url]").focus()
	});
};
rh.wp.enableButtons = function() {
	$("#toggle-edit").click(function() {
		if (rh.wp.editing) {
			rh.wp.editing = false;
			$(".edit-actions").addClass("hidden");
			$(this).html("Edit");
		} else {
			rh.wp.editing = true;
			$(".edit-actions").removeClass("hidden");
			$(this).html("Done");
		}
	});
	
	$("#add-weatherpic").click(function(){
		$("#insert-weatherpic-modal .modal-title").html("Add a Statue");
		$("#insert-weatherpic-modal button[type=submit]").html("Add a Statue");
		
		$("#insert-weatherpic-modal input[name=image]").val("");
		$("#insert-weatherpic-modal input[name=title]").val("");
		$("#insert-weatherpic-modal input[name=description]").val("");
		$("#insert-weatherpic-modal input[name=think]").val("");
		$("#insert-weatherpic-modal input[name=do]").val("");
		$("#insert-weatherpic-modal input[name=longitude]").val("");
		$("#insert-weatherpic-modal input[name=latitude]").val("");
		$("#insert-weatherpic-modal input[name=artist]").val("");
		$("#insert-weatherpic-modal input[name=entityKey]").val("").prop("disabled", true);
	});
	
	$(".edit-weatherpic").click(function(){
		$("#insert-weatherpic-modal .modal-title").html("Edit this Statue");
		$("#insert-weatherpic-modal button[type=submit]").html("Edit Statue");
		
		image = $(this).find(".image").html();
		title = $(this).find(".title").html();
		artist = $(this).find(".artist").html();
		description = $(this).find(".description").html();
		locationCoordinates = $(this).find(".location").html();
		entityKey = $(this).find(".entityKey").html();
		think = $(this).find(".think").html();
		do_text = $(this).find(".do").html();
		console.log("Text of think is " + think);
		console.log("Text of do is " + do_text);
		
		locationSplit = locationCoordinates.split(",");
		latitude = locationSplit[0];
		longitude = locationSplit[1].trim();
		//console.log(longitude);
		//console.log(latitude);
		
		
		$("#insert-weatherpic-modal input[name=image]").val(image);
		$("#insert-weatherpic-modal input[name=title]").val(title);
		$("#insert-weatherpic-modal input[name=artist]").val(artist);
		//$("#insert-weatherpic-modal input[name=longitude]").val(longitude);
		$("#insert-weatherpic-modal input[name=latitude]").val(latitude);
		$("#insert-weatherpic-modal input[name=longitude]").val(longitude);
		$("#insert-weatherpic-modal input[name=description]").val(description);
		$("#insert-weatherpic-modal input[name=think]").val(think);
		$("#insert-weatherpic-modal input[name=do]").val(do_text);
		$("#insert-weatherpic-modal input[name=entityKey]").val(entityKey).prop("disabled", false);
		
	});
	
	$(".delete-weatherpic").click(function(){
		entityKey = $(this).find(".entityKey").html();
		$("#delete-weatherpic-modal input[name=entityKey]").val(entityKey);
	});
};

$(document).ready(function(){
	rh.wp.enableButtons();
	rh.wp.attachEventHandlers();
});

//$("#toggle-edit").click(function() {
//	$(".edit-actions").toggleClass("hidden")
//});

