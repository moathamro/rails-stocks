function openForm() {
    document.getElementById("myForm").style.display = "block";
}

function closeForm() {
    document.getElementById("myForm").style.display = "none";
}

function openCheckbox() {
    document.getElementById("myCheckbox").style.display = "block";
}

function closeCheckbox() {
    document.getElementById("myCheckbox").style.display = "none";
}

$('#main-Form').submit(function(e) {
    if(cheackdata()){
        e.preventDefault();
    }
});


function cheackdata(event) {

    var searched = $("[name='stock_name']").val();

    if ($('#symbol-checkbox').is(":checked")) {
        if (/[^a-zA-Z]/.test(searched)) {
            alert("please enter a letters");
            return true
        }
    } else if ($('#name-checkbox').is(":checked")) {
        if (/[^a-zA-Z]/.test(word)) {
            alert("please enter a letters")
            return true
        }
    } else if ($('#price-checkbox').is(":checked")) {
        if (!$.isNumeric(searched)) {
            alert("please enter numbers")
            return true
        }
    } else if ($('#change-checkbox').is(":checked")) {

    }
}

function deleteinput(){
        document.getElementById("input-search").style.display = "none";
}

function getinput(){
        document.getElementById("input-search").style.display = "block";
}
// $( "tr" ).hover(
//   function() {
//     $( this ).append( $( "<span> ***</span>" ) );
//   }, function() {
//     $( this ).find( "span" ).last().remove();
//   }
// );