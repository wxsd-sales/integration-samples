function setDivSuccess(selector){
  $(selector).removeClass('alert-primary');
  $(selector).addClass('alert-success');
  $(selector).removeClass('enable-cursor');
  $(selector).addClass('default-cursor');
}

$('document').ready(function() {

  $('#webexAvatar').attr('src', webexAvatar);

  if(msftUser != "None"){
    setDivSuccess('#msftSignInDiv');
    $('#msftSignInDiv').html('Successfully Signed in to Microsoft Azure!');
    $('#msftCompleteImg').show();
  } else {
    $('#msftSignInDiv').on('click', function(){
      window.location = msftPath;
    })
  }

  if(zoomUser != "None"){ //if user is signed into Zoom.
    setDivSuccess('#zoomSignInDiv');
    $('#zoomSignInDiv').html('Successfully Signed in to Zoom!');
    $('#zoomCompleteImg').show();
  } else { // else, user is not signed into Zoom.
    $('#zoomSignInDiv').on('click', function(){
      window.location = zoomPath;
    })
  }
})
