
const options = {
    responsive = true
}

//Make user percent daily intake
console.log(hello)
let ctx = $("myChart").get(0).getContext('2d');

$.get('/user_dashboard.json', function(data) {
    let myChart = new Chart(ctx, {
        type: 'pie',
        data: data,
        options: options
    });
});
