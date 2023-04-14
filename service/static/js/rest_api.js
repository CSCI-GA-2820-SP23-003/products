$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#product_id").val(res.id);
        $("#product_name").val(res.name);
        $("#product_desc").val(res.desc);
        $("#product_price").val(res.price);
        $("#product_category").val(res.category);
        $("#product_inventory").val(res.inventory);
        $("#product_discount").val(res.discount);
        $("#product_like").val(res.like);
        $("#product_created_date").val(res.created_date);
        $("#product_modified_date").val(res.modified_date);
        $("#product_deleted_date").val(res.deleted_date);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#product_id").val(res.id);
        $("#product_name").val("");
        $("#product_desc").val("");
        $("#product_price").val("");
        $("#product_category").val("");
        $("#product_inventory").val("");
        $("#product_discount").val("");
        $("#product_like").val("");
        $("#product_created_date").val("");
        $("#product_modified_date").val("");
        $("#product_deleted_date").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Product
    // ****************************************

    $("#create-btn").click(function () {

        let product_id = $("#product_id").val();
        let name = $("#product_name").val();
        let desc = $("#product_desc").val();
        let price = $("#product_price").val();
        let category = $("#product_category").val();
        let inventory = $("#product_inventory").val();
        let discount = $("#product_discount").val();
        let like = $("#product_like").val();
        let created_date = $("#product_created_date").val();

        let data = {
            "id": product_id,
            "name": name,
            "desc": desc,
            "price": price,
            "category": category,
            "inventory": inventory,
            "discount": discount,
            "like": like,
            "created_date": created_date
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/products",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Product
    // ****************************************

    $("#update-btn").click(function () {

        let product_id = $("#product_id").val();
        let name = $("#product_name").val();
        let desc = $("#product_desc").val();
        let price = $("#product_price").val();
        let category = $("#product_category").val();
        let inventory = $("#product_inventory").val();
        let discount = $("#product_discount").val();
        let like = $("#product_like").val();
        let created_date = $("#product_created_date").val();
        let modified_date = $("#product_modified_date").val();
        let deleted_date = $("#product_deleted_date").val();

        let data = {
            "id": product_id,
            "name": name,
            "desc": desc,
            "price": price,
            "category": category,
            "inventory": inventory,
            "discount": discount,
            "like": like,
            "created_date": created_date,
            "modified_date": modified_date,
            "deleted_date": deleted_date
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/products/${product_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Product
    // ****************************************

    $("#retrieve-btn").click(function () {

        let product_id = $("#product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/products/${product_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Product
    // ****************************************

    $("#delete-btn").click(function () {

        let product_id = $("#product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/products/${product_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Product has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#product_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Product
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#product_name").val();
        let category = $("#product_category").val();
        let price = $("#product_price").val();

        let queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }
        if (price) {
            if (queryString.length > 0) {
                queryString += '&price=' + price
            } else {
                queryString += 'price=' + price
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/products?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Category</th>'
            table += '<th class="col-md-2">Available</th>'
            table += '<th class="col-md-2">Gender</th>'
            table += '<th class="col-md-2">Birthday</th>'
            table += '</tr></thead><tbody>'
            let firstProduct = "";
            for(let i = 0; i < res.length; i++) {
                let product = res[i];
                table +=  `<tr id="row_${i}"><td>${product.id}</td><td>${product.name}</td>td>${product.desc}</td>td>${product.price}</td><td>${product.category}</td><td>${product.inventory}</td><td>${product.discount}</td><td>${product.like}</td>td>${product.created_date}</td>td>${product.modified_date}</td>td>${product.deleted_date}</td></tr>`;
                if (i == 0) {
                    firstProduct = product;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstProduct != "") {
                update_form_data(firstProduct)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
