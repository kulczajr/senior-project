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
		$("#insert-weatherpic-modal .modal-title").html("Add a Weatherpic");
		$("#insert-weatherpic-modal button[type=submit]").html("Add a Weatherpic");
		
		$("#insert-weatherpic-modal input[name=image_url]").val("");
		$("#insert-weatherpic-modal input[name=caption]").val("");
		$("#insert-weatherpic-modal input[name=entity_key]").val("").prop("disabled", true);
	});
	
	$(".edit-weatherpic").click(function(){
		$("#insert-weatherpic-modal .modal-title").html("Edit this Weatherpic");
		$("#insert-weatherpic-modal button[type=submit]").html("Edit Weatherpic");
		
		image_url = $(this).find(".image").html();
		caption = $(this).find(".title").html();
		entityKey = $(this).find(".entity-key").html();
		
		$("#insert-weatherpic-modal input[name=image]").val(image_url);
		$("#insert-weatherpic-modal input[name=title]").val(caption);
		$("#insert-weatherpic-modal input[name=entity_key]").val(entityKey).prop("disabled", false);
		
	});
	
	$(".delete-weatherpic").click(function(){
		entityKey = $(this).find(".entity-key").html();
		$("#delete-weatherpic-modal input[name=entity_key]").val(entityKey);
	});
};

$(document).ready(function(){
	rh.wp.enableButtons();
	rh.wp.attachEventHandlers();
});

//$("#toggle-edit").click(function() {
//	$(".edit-actions").toggleClass("hidden")
//});

