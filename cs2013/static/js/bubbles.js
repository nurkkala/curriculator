var width = 550,
    height = 400,
    radius = Math.min(width, height) / 2;

var color = d3.scale.category20c();

var arc = d3.svg.arc()
      .outerRadius(radius * 0.8)
      .innerRadius(radius * 0.6);

var outerArc = d3.svg.arc()
      .outerRadius(radius * 0.9)
      .innerRadius(radius * 0.9);

function count_cs2013_outcomes(d) {
  return d.outcomes.length;
}

function count_cse_outcomes(d) {
  var count = 0;
  for (course in d.courses) {
    count += d.courses[course].outcomes.length;
  }
  return count;
}

var tu_cse_pie = d3.layout.pie()
      .sort(null)
      .value(count_cse_outcomes);

var cs2013_pie = d3.layout.pie()
      .sort(null)
      .value(count_cs2013_outcomes);

function bubble(dom_id, tier, pie_layout, outcome_counter) {
  var svg = d3
	.select(dom_id)
	.append("svg")
	.attr("width", width)
	.attr("height", height)
	.append("g")
	.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

  svg.append("g").attr("class", "slices");
  svg.append("g").attr("class", "labels");
  svg.append("g").attr("class", "lines");

  d3.json("/cs2013/api/coverage/" + tier + "/", function (error, data) {

    // Total outcomes
    var total_outcomes = 0;
    _.forEach(data, function(d) {
      total_outcomes += outcome_counter(d);
    });
    console.log(outcome_counter);
    svg.select(".slices")
      .append("text")
      .style("text-anchor", "middle")
      .style("font-size", "44px")
      .text(total_outcomes);

    // Slices
    var slice = svg.select(".slices")
	  .selectAll("path.slice")
	  .data(pie_layout(data));

    slice.enter()
      .insert("path")
      .style("fill", function(d, i) {
	return color(i);
      })
      .attr("class", "slice")
      .on("click", function(d, i) {
	location.href = "/cs2013/know-area/" + d.data.id + "/";
      });

    slice
      .transition().duration(1000)
      .attrTween("d", function(d) {
	this._current = this._current || d;
	var interpolate = d3.interpolate(this._current, d);
	this._current = interpolate(0);
	return function(t) {
	  return arc(interpolate(t));
	};
      });

    slice.exit().remove();

    // Labels
    var text = svg.select(".labels")
	  .selectAll("text")
	  .data(pie_layout(data));

    text.enter()
      .append("text")
      .attr("dy", ".35em")
      .text(function(d) {
	return d.data.abbreviation + " (" + outcome_counter(d.data) + ")";
      });

    function midAngle(d){
      return d.startAngle + (d.endAngle - d.startAngle)/2;
    }

    text.transition().duration(1000)
      .attrTween("transform", function(d) {
	this._current = this._current || d;
	var interpolate = d3.interpolate(this._current, d);
	this._current = interpolate(0);
	return function(t) {
	  var d2 = interpolate(t);
	  var pos = outerArc.centroid(d2);
	  pos[0] = radius * (midAngle(d2) < Math.PI ? 1 : -1);
	  return "translate("+ pos +")";
	};
      })
      .styleTween("text-anchor", function(d){
	this._current = this._current || d;
	var interpolate = d3.interpolate(this._current, d);
	this._current = interpolate(0);
	return function(t) {
	  var d2 = interpolate(t);
	  return midAngle(d2) < Math.PI ? "start":"end";
	};
      });

    text.exit().remove();

    // Lines
    var polyline = svg.select(".lines")
	  .selectAll("polyline")
	  .data(pie_layout(data));

    polyline.enter()
      .append("polyline");

    polyline.transition().duration(1000)
      .attrTween("points", function(d){
	this._current = this._current || d;
	var interpolate = d3.interpolate(this._current, d);
	this._current = interpolate(0);
	return function(t) {
	  var d2 = interpolate(t);
	  var pos = outerArc.centroid(d2);
	  pos[0] = radius * 0.95 * (midAngle(d2) < Math.PI ? 1 : -1);
	  return [arc.centroid(d2), outerArc.centroid(d2), pos];
	};
      });

    polyline.exit().remove();
  });
}

bubble("#cs2013-1", 1, cs2013_pie, count_cs2013_outcomes);
bubble("#cs2013-2", 2, cs2013_pie, count_cs2013_outcomes);
bubble("#cs2013-3", 3, cs2013_pie, count_cs2013_outcomes);

bubble("#tu-cse-1", 1, tu_cse_pie, count_cse_outcomes);
bubble("#tu-cse-2", 2, tu_cse_pie, count_cse_outcomes);
bubble("#tu-cse-3", 3, tu_cse_pie, count_cse_outcomes);

d3.json("/cs2013/api/coverage/1/", function (error, data) {
  d3.select("#legend")
    .selectAll("li")
    .data(data)
    .enter()
    .append("li")
    .text(function (d) { return d.abbreviation + " - " + d.name; });
});
