'use strict';



// Manipulating the DOM

// The goal here is to learn about or use innerText or or innerHTML


let signInButton = document.querySelector("#signIn");

signInButton.addEventListener("click", function () {
  if (signInButton.innerText === "Log In") {
    signInButton.innerText = "Log Out";
  } else {
    signInButton.innerText = "Log In";
  }
});



// Preventing Form Submission


let stalledForm = document.querySelector("#prevent-form-submission-form");

stalledForm.addEventListener("submit", function (evt) {
  evt.preventDefault();
  alert("Better luck next time!");
});



// AJAX

function getPlanetInfo(){
    $.get("https://swapi.co/api/planets/1/", showResults)
  }

function showResults(results) {
  $('#climate').html(results.climate);
  $('#terrain').html(results.terrain);
  $('#population').html(results.population);
}

// Alternate
// function showResults(results){
//     for (let result in results) {
//       $('#' + result).html(results[result]);
//     }
// }

$("#getInfo").on("click", getPlanetInfo);
