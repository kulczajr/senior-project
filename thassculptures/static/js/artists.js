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
		$("#insert-weatherpic-modal .modal-title").html("Add an Artist");
		$("#insert-weatherpic-modal button[type=submit]").html("Add Arist");
		
		$("#insert-weatherpic-modal input[name=fname]").val("");
		$("#insert-weatherpic-modal input[name=lname]").val("");
		$("#insert-weatherpic-modal input[name=image]").val("");
		$("#insert-weatherpic-modal input[name=website_url]").val("");
		$("#insert-weatherpic-modal input[name=description]").val("");
		$("#insert-weatherpic-modal input[name=entityKey]").val("").prop("disabled", true);
	});
	
	$(".edit-weatherpic").click(function(){
		$("#insert-weatherpic-modal .modal-title").html("Edit this Artist");
		$("#insert-weatherpic-modal button[type=submit]").html("Edit Artist");
		
		description = $(this).find(".description").html();
		entityKey = $(this).find(".entityKey").html();
		fname = $(this).find(".fname").html();
		lname = $(this).find(".lname").html();
		website_url = $(this).find(".website_url").html();
		image = $(this).find(".image").html();
		
		$("#insert-weatherpic-modal input[name=description]").val(description);
		$("#insert-weatherpic-modal input[name=fname]").val(fname);
		$("#insert-weatherpic-modal input[name=lname]").val(lname);
		$("#insert-weatherpic-modal input[name=website_url]").val(website_url);
		$("#insert-weatherpic-modal input[name=image]").val(image);
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

