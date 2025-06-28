
$(document).ready(function(){
    $(".ajaxLoader").hide();
	// Product Filter Categories & Brands Start
    $(".filter-checkbox, #priceFilterBtn").on('click', function(){
        var filter_object={};
        var minPrice=$('#maxPrice').attr('min');
        var maxPrice=$('#maxPrice').val();
        filter_object.minPrice=minPrice;
        filter_object.maxPrice=maxPrice;
        $(".filter-checkbox").each(function(index, ele){
            var filter_value=$(this).val();
            var filter_key=$(this).data('filter');
            filter_object[filter_key]=Array.from(document.querySelectorAll('input[data-filter='+filter_key+']:checked')).map(function(el){
                return el.value;
           });
        });

        // Run Ajax
        $.ajax({
            url:"/filter_data/",
            method:"GET",
            data:filter_object,
            dataType:"json",
            beforeSend:function(){
				$(".ajaxLoader").show();
			},
            success:function(res){				
                $("#filteredProducts").html(res.products);
                $(".ajaxLoader").hide();
            },
        });
        console.log("Clicked", minPrice, maxPrice, 'Filter Object', filter_object);
    });
    // Product Filter Categories & Brands End
    
    // Filter Product According to the price
    $("#maxPrice").on('blur',function(){
        var min=$(this).attr('min');
        var max=$(this).attr('max');
        var value=$(this).val();
        if(value < parseInt(min) || value > parseInt(max)){
            alert('Values should be '+min+'-'+max);
            $(this).val(min);
            $(this).focus();
            $("#rangeInput").val(min);
            return false;
        }
        console.log("Iam MinPrice MaxPrice",value,min,max);
    });
    // Filter Product According to the price End

    // Product pagination Start
    $("#loadMore").on('click', function(){
        var currentProducts=$(".product-box").length;
        var limit=$(this).attr('data-limit');
        var total=$(this).attr('data-total');
        
        // Run Ajax
        $.ajax({
            url:"/load_more_data/",
            method:"GET",
            data:{offset:currentProducts,limit:limit},
            dataType:"json",
            beforeSend:function(){
                $("#loadMore").attr('disabled',true);
				$(".load-more-icon").addClass('fa-spin');
			},
            success:function(res){	
                $("#filteredProducts").append(res.products);			
				$("#loadMore").attr('disabled',false);
				$(".load-more-icon").removeClass('fa-spin');

                var totalShowing=$(".product-box").length;
				if(totalShowing==total){
					$("#loadMore").remove();
				}
            },
        });
        console.log(currentProducts,limit,total);
    });
    // Product pagination end
});