function initRecaptcha() {

  var container = document.getElementById('recaptcha-container');
  if (!container) return;
  

  grecaptcha.render('recaptcha-container', {
    'sitekey': '6LcK7CIrAAAAANRkAK8mITnUqkH9DlMC2I2gsVsF',
    'callback': function(response) {
      console.log('CAPTCHA completed');
    }
  });
}

(function() {
  var recaptchaScript = document.createElement('script');
  recaptchaScript.src = 'https://www.google.com/recaptcha/api.js?onload=initRecaptcha&render=explicit';
  recaptchaScript.async = true;
  recaptchaScript.defer = true;
  document.head.appendChild(recaptchaScript);
})();


document.addEventListener('DOMContentLoaded', function() {
  var productForm = document.getElementById('productContactForm');
  if (productForm) {
    productForm.addEventListener('submit', function(event) {
      if (typeof grecaptcha !== 'undefined' && grecaptcha.getResponse() === '') {
        event.preventDefault();
        alert('CAPTCHA verification requested');
      }
    });
  }
});
