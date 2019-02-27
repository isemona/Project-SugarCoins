var margin = {top: 20, right: 20, bottom: 30, left: 30},
    width = 500 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var dataset = [
  {x: 0.4, y: 0.6, r: 0.3, label: "Scubadiving"},
  {x: 0.7, y: 0.5, r: 0.95, label: "Rollerblading"},
  {x: 0.0, y: 0.5, r: 0.98, label: "Swimming"},
  {x: 1.0, y: 0.7, r: 0.7, label: "Weightlifting"},
  {x: 0.2, y: 0.0, r: 0.4, label: "Running"},
  {x: 0.2, y: 1.0, r: 0.3, label: "Yoga"}
];

var xScale = d3.scale.linear()
    .range([0, width]);

var yScale = d3.scale.linear()
    .range([height, 0]);

var rScale = d3.scale.pow()
    .exponent(0.7)
    .range([0, 0.08*(width+height)]);

var colorScale = d3.scale.category20c();

var xAxis = d3.svg.axis()
    .scale(xScale)
    .orient("bottom")
    .tickSize(-height)
    .ticks(2)
    .tickPadding(12)
    .tickFormat(function(val) {
      return (val === 0.5) ?
          'Session Count' :
        (val === 0) ?
          'Low' :
          "High";
    });

var yAxis = d3.svg.axis()
    .scale(yScale)
    .orient("bottom")
    .tickSize(-width)
    .ticks(2)
    .tickPadding(12)
    .tickFormat(function(val) {
      return (val === 0.5) ?
          'Correlation' :
        (val === 0) ?
          'Low' :
          "High";
    });

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .attr("transform", "rotate(90)")
      .call(yAxis)
      .selectAll("text")
      .attr("y", function() { return -d3.select(this).attr("y"); })
      .attr("dy", "0em")
      .attr("transform", "rotate(180)");

  svg.append("g")
      .attr("class", "quadrant-labels")
      .selectAll("text")
      .data([[0.25,0.25,"Lame"],
            [0.75,0.25,"Often"],
            [0.25,0.75,"Promising"],
            [0.75,0.75,"Superb"]])
      .enter()
      .append("text")
      .each(function(d) { console.info(d); })
      .attr("x", function(d) { return xScale(d[0]); })
      .attr("y", function(d) { return yScale(d[1]); })
      .attr("text-anchor", "middle")
      .attr("dy", ".35em")
      .text(function(d) { return d[2]; });

  var circleSelection = svg.append("g")
      .selectAll("g")
      .data(dataset)
      .enter()
      .append("g")
      .attr("transform", function(d) {
        var x = -2*(d.x-0.5) * rScale(d.r) + xScale(d.x),
            y = 2*(d.y-0.5) * rScale(d.r) + yScale(d.y);

        return "translate("+[x, y]+")";
      })
      .attr("class", "circle");

  circleSelection.append("circle")
      .attr("r", function(d) { return rScale(d.r); })
      .attr("stroke", function(d) { return colorScale(d.x*d.y*d.r); })
      .attr("fill", function(d) { return colorScale(d.x*d.y*d.r); });

  circleSelection.append("text")
      .text(function(d) { return d.label; })
      .attr("font-size", 10)
      .attr("text-anchor", "middle")
      .attr("font-size", function(d) { return Math.min(1.8*rScale(d.r), (1.8*rScale(d.r)) / this.getComputedTextLength() * 10); })
      .attr("dy", ".35em");
