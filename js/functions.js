$(window).scroll(function(){
  var wScroll = $(this).scrollTop();
  console.log(wScroll)

  $('.logo').css({
    'transform' : 'translate(0px,'+ wScroll /2+'%)'
  });

  $('.fore-baloon').css({
    'transform' : 'translate('+ wScroll /10 +'%,'+ wScroll /4 +'%)'
  });

  $('.back-baloon2').css({
    'transform' : 'translate('+ wScroll /10 +'%,'+ wScroll /4 +'%)'
  });

  $('.back-baloon').css({
    'transform' : 'translate(0px,'+ wScroll /100+'%)'
  });

  });

  $('a').click(function(){
    $('html, body').animate({
        scrollTop: $( $.attr(this, 'href') ).offset().top
    }, 500);
    return false;
});
