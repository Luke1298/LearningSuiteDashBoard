var letter_grade_classifier = function(data){
    var greatest_bigger = 0;
    var to_return;
    console.log(data.grade_scale);
    for (var key in data.grade_scale){
        //console.log(data.course_grade);
        //console.log(key);
        if (parseFloat(data.course_grade) > parseFloat(data.grade_scale[key])){
            if (parseFloat(data.grade_scale[key]) > greatest_bigger){
                greatest_bigger = parseFloat(data.grade_scale[key]);
                console.log(key);
                to_return=key;
            }
        }
    }
    return to_return;
}

var letter_grade_to_color = function(letter){
    if (letter == "A" || letter=="A-"){
        return "green";
    }
    else if (letter == "B+" || letter == "B" || letter == "B-"){
        return "blue";
    }
    else if (letter == "C+" || letter == "C" || letter == "C-"){
        return "yellow";
    }
    else if (letter == "D+" || letter == "D" || letter == "D-" || letter == "E"){
        return "red";
    }
    else{
        return "red";
    }
}


var build_grades_table = function(data){
    var width = document.getElementById("grades").offsetWidth;
    var gap = 7;
    var bar_height = 34;
    var height = (bar_height + gap * 2) * data.length + 12;
    var chart;
    var x, y;
    chart = d3.select($("#grades")[0])
      .append('svg')
      .attr('id', 'grades-svg')
      .attr('class', 'chart')
      .attr('width', "100%")
      .attr('height', height)
      .attr("preserveAspectRatio", "xMinYMin meet")
      .attr("viewBox", "0 0 "+ String(width) + " " + String(height))
      .classed("svg-content-responsive", true)
      .append("g")
      .attr("transform", "translate(0, 20)");


    console.log($("#grades-svg")[0])

    var cid_list = [];
    for (i = 0; i < data.length; i++) {
        cid_list.push(data[i].cid);
    }


    x = d3.scale.linear()
        .domain(d3.range(0, width));

    y = d3.scale.ordinal()
        .domain(cid_list)
        .rangeBands([0, (bar_height + 2 * gap) * data.length])


    console.log(y.rangeBand());

    chart.selectAll("line")
      .data([1,2,3,4,5,6,7,8,9,10])
      .enter().append("line")
      .attr("x1", function(d) { return d*10*width/100.0;})
      .attr("x2", function(d) { return d*10*width/100.0;})
      .attr("y1", 0)
      .attr("y2", (bar_height + gap * 2) * data.length)
      .style("stroke", "grey");

    chart.selectAll(".rule")
      .data([1,2,3,4,5,6,7,8,9,10])
      .enter().append("text")
      .attr("class", "rule")
      .attr("x", function(d) { return d*10*width/100.0; })
      .attr("y", 0)
      .attr("dy", -6)
      .attr("dx", function(d){
        // HACK FOR OVER EXTENDED 100
        if (d*10 == 100){
            return -13;
        }
        else{
            return 0;
        }
      })
      .attr("text-anchor", "middle")
      .attr("font-size", 10)
      .text(function(d) { return String(d*10)+"%";});


    chart.selectAll("rect")
       .data(data)
       .enter().append("rect")//DEPEND UPON PERCENTAGE
       .attr("x", 0)
       .attr("y", function(d) { return y(d.cid) + gap;})
       .attr("width", function(d) { return parseFloat(d.course_grade)*(width/100.0);})
       .attr("height", bar_height);

    chart.selectAll("rect")
      .data(data)
      .attr("class", function(d){ return letter_grade_to_color(letter_grade_classifier(d))});

    var class_title_tip = d3.tip()
      .attr('class', 'd3-tip2')
      .offset([-gap/2, 0])
      .html(function(d) {
        return "<strong class='grade-tool-tip'>" + d.course_title + "</strong>";
      })

    chart.call(class_title_tip);

    chart.selectAll("text.name")
      .data(data)
      .enter().append("text")
      .attr("x", 12)
      .attr("y", function(d){ return y(d.cid) + y.rangeBand()/2; } )
      .attr("dy", ".36em")
      .attr("text-anchor", "left")
      .attr('class', 'course-code')
      .on('mouseover', class_title_tip.show)
      .on('mouseout', class_title_tip.hide)
      .text(function(d){ return d.course_code + " (" + d.course_grade  + ") "});

    w = d3.scale.ordinal()
        .domain(["footer"])
        .rangeBands([0, (bar_height + 2 * gap)])

    key = d3.select($("#grade-key")[0])
      .append('svg')
      .attr('id', 'grades-svg')
      .attr('class', 'key')
      .attr('width', "100%")
      .attr('height', bar_height)
      .attr("preserveAspectRatio", "xMinYMin meet")
      .attr("viewBox", "0 0 "+ String(width) + " " + String(bar_height))
      .classed("svg-content-responsive", true)

    key.selectAll("rect")
       .data([0,1,2,3])
       .enter().append("rect")//DEPEND UPON PERCENTAGE
       .attr("x", function(d){ console.log(d*25*width/100.0); return d*25*width/100.0+gap*2;})
       .attr("y", 0)
       .attr("class", function(d){
           if (d==0){
               return "green";
           }
           if (d==1){
               return "blue";
           }
           if (d==2){
               return "yellow";
           }
           if (d==3){
               return "red";
           }
       })
       .attr("width", function(d) { return 25*width/100.0;})
       .attr("height", bar_height)

    key.selectAll("text")
      .data([0,1,2,3])
      .enter().append("text")
      .attr("x", function(d){ return 25*width/200.0 + d*25*width/100.0+gap*2;})
      .attr("y", bar_height/2)
      .attr("dy", ".36em")
      .attr("text-anchor", "left")
      .attr('class', 'course-code')
      .on('mouseover', class_title_tip.show)
      .on('mouseout', class_title_tip.hide)
      .text(function(d){
          if (d == 0){
              return "A";
          }
          if (d == 1){
              return "B";
          }
          if (d == 2){
              return "C";
          }
          if (d == 3){
              return "D";
          }
      });
    /*key.selectAll("rt")
      .enter().append("rect")
      .attr("class", "rule")
      .attr("x", function(d) {d*25})
      .attr("y", 0)
      .attr("text-anchor", "middle")
      .attr("font-size", 10)
      .text(function(d) { return String(d*10)+"%";});*/
}
