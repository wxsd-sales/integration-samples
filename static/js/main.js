function setDivSuccess(selector){
  $(selector).removeClass('alert-primary');
  $(selector).addClass('alert-success');
  $(selector).removeClass('enable-cursor');
  $(selector).addClass('default-cursor');
}

function setDivReady(selector){
  $(selector).removeClass('alert-secondary');
  $(selector).addClass('alert-primary');
  $(selector).removeClass('disable-cursor');
  $(selector).addClass('enable-cursor');
}

$('document').ready(function() {

  $('#webexAvatar').attr('src', webexAvatar);

  if(msftUser != "None"){
    setDivSuccess('#msftSignInDiv');
    $('#msftSignInDiv').html('Successfully Signed in to Microsoft Outlook!');
    $('#msftSignInDiv').removeClass('disable-cursor');
    $('#msftCompleteImg').show();
    $('#msftNextStepImg').hide();
  } else {
    $('#msftSignInButton').prop('disabled', true);
  }

  if(zoomUser != "None"){ //if user is signed into Zoom.
    setDivSuccess('#zoomSignInDiv');
    $('#zoomSignInDiv').html('Successfully Signed in to Zoom!');
    $('#zoomCompleteImg').show();
    $('#zoomNextStepImg').hide();

    if(msftUser != "None"){
      setDivReady('#searchMeetingsDiv');
    } else {
      setDivReady('#msftSignInDiv');
      $('#msftNextStepImg').show();
      $('#msftSignInButton').prop('disabled', false);
      $('#msftSignInDiv').on('click', function(){
        window.location = msftPath;
      })
    }
  } else { // else, user is not signed into Zoom.
    $('#zoomSignInDiv').on('click', function(){
      window.location = zoomPath;
    })
  }
})
