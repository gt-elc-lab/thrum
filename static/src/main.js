function Input() {
        var tech;
        var uga;
        var word;

        var setTech = function(school) {
            tech = school;
        };

        var getTech = function() {
            return tech;
        };

        var setUga = function(school) {
            uga = school;
        };

        var getUga = function() {
            return uga;
        };

        var setWord = function(text) {
            word = text;
        };

        var getWord = function() {
            return word;
        };

        var graph = function() {
            if (!tech || !uga) {
                alert('Please select two schools');
                return;
            }
            if (!word) {
                alert('Please enter a word');
                return;
            }
            var url = 'data/' + input.getTech()+'/' + input.getUga() + '/' + input.getWord();
            drawGraph(tech, uga, word);
        };

        return {
            setTech: setTech,
            setUga: setUga,
            setWord: setWord,
            graph: graph,
            getTech: getTech,
            getUga: getUga,
            getWord: getWord
        };
    }

var input = new Input();

function setTech(school) {
    input.setTech(school);
}

function setUga(school) {
    input.setUga(school);
}

function setWord() {
    var word = document.getElementById('text').value;
    input.setWord(word);
}

function graph() {
    setWord();
    input.graph();
}

function drawGraph(tech, uga, word) {

    var url = 'data/' + tech+'/' + uga + '/' + word;
    document.getElementById('line-graph').innerHTML = "";
    var margin = {top: 30, right: 20, bottom: 30, left: 50},
    width = 1080 - margin.left - margin.right,
    height = 550 - margin.top - margin.bottom;


var x = d3.time.scale()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var line = d3.svg.line()
    .x(function(d) { return x(new Date(d.date)); })
    .y(function(d) { return y(d.count); })
    .interpolate('basis');

var svg = d3.select("#line-graph").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.json(url, function(error, response) {
 
  var data = response['tech'];
  var data2 = response['uga'];
  
  x.domain(d3.extent(data, function(d) { return new Date(d.date); }));
  y.domain(d3.extent(data, function(d) { return d.count; }));

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Frequency");

  svg.append("path")
      .datum(data)
      .attr('class', 'line')
      .attr('d', line(data))
      .style('fill', 'none')
      .style('stroke', '#FB5050')
      .style('stroke-width', '3px');

 x.domain(d3.extent(data2, function(d) { return new Date(d.date); }));
 y.domain(d3.extent(data2, function(d) { return d.count; }));
svg.append("path")
      .datum(data2)
      .attr('class', 'line')
      .attr('d', line(data2))
      .style('fill', 'none')
      .style('stroke', '#FACA50')
      .style('stroke-width', '3px');

svg.append("text")
        .attr("x", (width / 2))             
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")  
        .style("font-size", "16px") 
        .style("text-decoration", "underline")  
        .text(tech + ' vs. ' + uga);

// svg.selectAll("circle.line")
//         .data(data)
//         .enter().append("svg:circle")
//         .attr("class", "line")
//         .style("fill", "green")
//         .attr("cx", valueline.x())
//         .attr("cy", valueline.y())
//         .attr("r", 3.5);
  });

}
