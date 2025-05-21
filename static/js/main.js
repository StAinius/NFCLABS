setTimeout(function() {
    var messageElement = document.getElementById('success-message');
    if (messageElement) { 
        messageElement.style.transition = 'opacity 0.5s ease';
        messageElement.style.opacity = '0';
            
    setTimeout(function() {
        messageElement.remove();
        }, 500);
    }
}, 5000);
