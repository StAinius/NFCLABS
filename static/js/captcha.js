document.addEventListener('DOMContentLoaded', function() {
  var recaptchaScript = document.createElement('script');
  recaptchaScript.src = 'https://www.google.com/recaptcha/api.js?onload=initRecaptcha&render=explicit';
  recaptchaScript.async = true;
  recaptchaScript.defer = true;
  document.head.appendChild(recaptchaScript);
  
  var successMessage = document.getElementById('successMessage');
  if (!successMessage) {
    successMessage = document.createElement('div');
    successMessage.id = 'successMessage';
    successMessage.className = 'alert alert-success';
    successMessage.innerText = 'Message sent successfully!';
    successMessage.style.position = 'fixed';
    successMessage.style.top = '20px';
    successMessage.style.left = '50%';
    successMessage.style.transform = 'translateX(-50%)';
    successMessage.style.padding = '15px 30px';
    successMessage.style.borderRadius = '5px';
    successMessage.style.zIndex = '9999';
    successMessage.style.backgroundColor = '#d4edda';
    successMessage.style.color = '#155724';
    successMessage.style.border = '1px solid #c3e6cb';
    successMessage.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
    successMessage.style.display = 'none';
    document.body.appendChild(successMessage);
  }
  
  var errorMessage = document.createElement('div');
  errorMessage.className = 'alert alert-danger';
  errorMessage.innerText = 'Failed to send message. Please try again.';
  errorMessage.style.position = 'fixed';
  errorMessage.style.top = '20px';
  errorMessage.style.left = '50%';
  errorMessage.style.transform = 'translateX(-50%)';
  errorMessage.style.padding = '15px 30px';
  errorMessage.style.borderRadius = '5px';
  errorMessage.style.zIndex = '9999';
  errorMessage.style.backgroundColor = '#f8d7da';
  errorMessage.style.color = '#721c24';
  errorMessage.style.border = '1px solid #f5c6cb';
  errorMessage.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
  errorMessage.style.display = 'none';
  document.body.appendChild(errorMessage);
  
  var isCaptchaVerified = false;
  var isPrivacyChecked = false;
  
  function updateSubmitButton() {
    var submitBtn = document.querySelector('button[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = !(isCaptchaVerified && isPrivacyChecked);
    }
  }
  
  var privacyCheckbox = document.getElementById('privacy');
  if (privacyCheckbox) {
    privacyCheckbox.addEventListener('change', function() {
      isPrivacyChecked = this.checked;
      updateSubmitButton();
    });
    
    isPrivacyChecked = privacyCheckbox.checked;
  }
  
  window.initRecaptcha = function() {
    var container = document.getElementById('recaptcha-container');
    if (!container) return;
    
    grecaptcha.render('recaptcha-container', {
      'sitekey': '6LcK7CIrAAAAANRkAK8mITnUqkH9DlMC2I2gsVsF',
      'callback': function(response) {
        isCaptchaVerified = !!response;
        updateSubmitButton();
      },
      'expired-callback': function() {
        isCaptchaVerified = false;
        updateSubmitButton();
      }
    });
    
    updateSubmitButton();
  };
  
  function showSuccessMessage() {
    successMessage.style.display = 'block';
    successMessage.style.opacity = '1';
    
    setTimeout(function() {
      successMessage.style.opacity = '0';
      successMessage.style.transition = 'opacity 0.5s ease';
      setTimeout(function() {
        successMessage.style.display = 'none';
        successMessage.style.opacity = '1';
      }, 500);
    }, 3000);
  }
  
  function showErrorMessage() {
    errorMessage.style.display = 'block';
    errorMessage.style.opacity = '1';
    
    setTimeout(function() {
      errorMessage.style.opacity = '0';
      errorMessage.style.transition = 'opacity 0.5s ease';
      setTimeout(function() {
        errorMessage.style.display = 'none';
        errorMessage.style.opacity = '1';
      }, 500);
    }, 3000);
  }
  
  // Ieškome visų formų su ID, kurie gali egzistuoti
  var contactForms = document.querySelectorAll('#contactForm, #ContactForm');
  
  contactForms.forEach(function(form) {
    if (form) {
      form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        if (typeof grecaptcha === 'undefined' || grecaptcha.getResponse() === '') {
          alert('Please verify that you are not a robot');
          return false;
        }
        
        if (privacyCheckbox && !privacyCheckbox.checked) {
          alert('Please agree to the privacy policy');
          return false;
        }
        
        var submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
          submitButton.disabled = true;
          var originalButtonText = submitButton.innerHTML;
          submitButton.innerHTML = '<i class="fa fa-spinner fa-spin me-2"></i>Sending...';
        }
        
        var formData = new FormData(this);
        
        // Pridedame AJAX antraštę, kad serveris žinotų, jog tai AJAX užklausa
        var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        fetch(this.action, {
          method: 'POST',
          body: formData,
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken
          }
        })
        .then(function(response) {
          console.log('Response status:', response.status);
          response.text().then(function(text) {
            console.log('Response text:', text);
          });
          
          if (response.ok) {
            showSuccessMessage();
            form.reset();
            if (typeof grecaptcha !== 'undefined') {
              grecaptcha.reset();
            }
            isCaptchaVerified = false;
            updateSubmitButton();
          } else {
            showErrorMessage();
          }
        })
        .catch(function(error) {
          console.error('Error:', error);
          showErrorMessage();
        })
        .finally(function() {
          if (submitButton) {
            submitButton.disabled = false;
            submitButton.innerHTML = originalButtonText;
          }
        });
      });
    }
  });
});