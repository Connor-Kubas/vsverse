window.addEventListener('load', function () {
  var modal = document.getElementById("modal");

  // Get the button that opens the modal
  var btn = document.getElementsByClassName("page-select-input-modal");

  // Get the <span> element that closes the modal
  // var span = document.getElementsByClassName("close")[0];

  // When the user clicks on the button, open the modal
  for (let i = 0; i < btn.length; i++) {
    btn[i].onclick = function() {
      modal.style.display = "flex";
    }
  }

  // When the user clicks on <span> (x), close the modal
  // span.onclick = function() {
  //   modal.style.display = "none";
  // }

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  } 
})



// function removeTableRow() {
//   const td = event.target.parentNode;
//   const tr = td.parentNode;
//   tr.parentNode.removeChild(tr);
// }