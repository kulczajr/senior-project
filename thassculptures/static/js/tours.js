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
		$("#insert-weatherpic-modal .modal-title").html("Add a Tour");
		$("#insert-weatherpic-modal button[type=submit]").html("Add a Tour");
		
		$("#insert-weatherpic-modal input[name=sculpture_list]").val("");
		$("#insert-weatherpic-modal input[name=description]").val("");
		$("#insert-weatherpic-modal input[name=entityKey]").val("").prop("disabled", true);
	});
	
	$(".edit-weatherpic").click(function(){
		$("#insert-weatherpic-modal .modal-title").html("Edit this Tour");
		$("#insert-weatherpic-modal button[type=submit]").html("Edit Tour");
		
		description = $(this).find(".description").html();
		entityKey = $(this).find(".entityKey").html();
		sculpture_list = $(this).find(".sculpture_list").html().split(",");
		
		console.log("Sculpture list is " + sculpture_list);
		
		//console.log(longitude);
		//console.log(latitude);
		console.log(sculpture_list);
		var sculptureDict = new Object();
		
		var sculptureTitles = [];
		var sculptureKeys = [];
		for (i = 0; i < sculpture_list.length; i++) { 
		    sculpture_title = sculpture_list[i].split("SEPERATOR")[0];
		    sculpture_key = sculpture_list[i].split("SEPERATOR")[1];
		    console.log("key is " + sculpture_key);
		    console.log("value is " + sculpture_title);
		    sculpture_title = sculpture_title.replace("u'", "");
		    sculpture_title = sculpture_title.replace("[", "");
		    sculptureDict[sculpture_key] = sculpture_title;
		}
		
		var $el = $("#current_sculptures");
		$el.empty(); // remove old options
		$.each(sculptureDict, function(value,key) {
		  $el.append($("<option></option>")
		     .attr("value", value).text(key));
		});
		
		$("#insert-weatherpic-modal input[name=description]").val(description);
		//$("#insert-weatherpic-modal input[name=sculpture_list]").val(sculpture_list);
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

