// Function to increment the card quantity
function incrementQuantity(deckId, cardId) {
    console.log('YUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUP');
    $.ajax({
        url: '/increment_quantity/' + deckId + '/' + cardId + '/',
        type: 'GET',
        success: function(response) {
            // Update the table display after successful increment
            $('#table-display').html(response)
        },
        error: function(error) {
            console.log(error);
        }
    });
}

// Function to decrement the card quantity
function decrementQuantity(deckId, cardId) {
    $.ajax({
        url: '/decrement_quantity/' + deckId + '/' + cardId + '/',
        type: 'GET',
        success: function(response) {
            // Update the table display after successful decrement
            updateTableDisplay();
        },
        error: function(error) {
            console.log(error);
        }
    });
}

// Event listener for adding a card
$('#add-card-button').on('click', function() {
    // Code to add the card to the deck
    console.log('hit');
    // Call the incrementQuantity method
    incrementQuantity(deckId, cardId);
});