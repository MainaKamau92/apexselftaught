function toggle() {
  var x = document.getElementById("toggleable-form");
  var btn = document.getElementById("dashboard-btn");
  if (x.style.display === "none") {
  x.style.display = "block";
    btn.textContent="Close"
    btn.setAttribute("class", "btn btn-danger");
  } else {
  x.style.display = "none";
  btn.textContent="Edit Info"
  btn.setAttribute("class", "btn btn-primary");
  
  }
}

$(document).delegate('#textbox', 'keydown', function(e) {
  var keyCode = e.keyCode || e.which;

  if (keyCode == 9) {
    e.preventDefault();
    var start = this.selectionStart;
    var end = this.selectionEnd;

    // set textarea value to: text before caret + tab + text after caret
    $(this).val($(this).val().substring(0, start)
                + "\t"
                + $(this).val().substring(end));

    // put caret at right position again
    this.selectionStart =
    this.selectionEnd = start + 1;
  }
});