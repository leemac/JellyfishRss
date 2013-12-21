function getCSRF()
{
  return document.getElementsByName('csrfmiddlewaretoken')[0].value;
}

$(function () {
  var App = new AppView();
});