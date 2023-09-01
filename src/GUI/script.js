$.ajax({
  type: "POST",
  url: "./plc_com_manager.py",
  data: { param: text }
}).done(function (o) {
  // do something
});



function pointing() {
  var azValue = document.querySelector(".az").value
  var elValue = document.querySelector(".el").value

  console.log(azValue)
  console.log(elValue)
}

