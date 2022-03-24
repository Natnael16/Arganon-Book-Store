window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    document.getElementById("navbar").style.display = "none";
    document.getElementById("navbar1").style.display = "none";
  } else {
    document.getElementById("navbar").style.display= "block";
    document.getElementById("navbar1").style.display = "none";
  }
}