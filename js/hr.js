/* 

Hover over the <hr /> tag to see the effect.

TO DO:
======

1. Add the option to make the <hr> element show progress automatically when the user scrolls past it.

2. Make the "time remaining" based on word count rather than % scrolled.

3. Clean up/organize the code. 

*/

var $el = $('.wrap'),
    wordCount = $el.text().trim().replace(/\s+/gi, ' ').split(' ').length,
    avgSpeed = 150,
    readTime = Math.round(wordCount/avgSpeed); 

// sets 
function hrHover(scrollPercent, currentReadTime){
  var scrollPercent = scrollPercent < 0 
    ? 0 
    : scrollPercent;
  $('hr.active')
    .css({
      'width': scrollPercent + '%'
    })
    .attr('data-percent', Math.round(scrollPercent) + '% complete')
    .attr('data-readtime', currentReadTime);
}

function hrVals() {
  var currY = $(this).scrollTop() - $('.hero').height(),
      postHeight = $(this).height(),
      scrollHeight = $el.height(),
      scrollPercent = (currY / (scrollHeight - postHeight)) * 100 < 100 
        ? (currY / (scrollHeight - postHeight)) * 100
        : 100,
      currentReadTime = Math.round(readTime - (readTime*(scrollPercent/100))) < 1
        ? 'Less than a minute remaining'
        : 'About ' + Math.round(readTime - (readTime*(scrollPercent/100))) + 'min remaining';
  
  hrHover(scrollPercent, currentReadTime);
}

$(window).on('scroll', hrVals);

$('hr')
  .on('mouseenter', function(){
    $(this).addClass('active');
    $('.explanation').hide();hrVals();
  }) 
  .on('mouseleave', function(){
    $(this)
      .removeClass('active')
      .css('width', '100%')
  })

$('h1').attr('data-timeToRead', 'By Friedrich Nietzsche • '+ Math.round(readTime) + ' min read'); 