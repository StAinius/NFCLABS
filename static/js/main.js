setTimeout(function () {
    var messageElement = document.getElementById('success-message');
    if (messageElement) {
        messageElement.style.transition = 'opacity 0.5s ease';
        messageElement.style.opacity = '0';

        setTimeout(function () {
            messageElement.remove();
        }, 500);
    }
}, 5000);


// Our products recommendations
const mobileProductCards = document.querySelectorAll('.mobile-product-card');

mobileProductCards.forEach(card => {
    card.addEventListener('click', function (e) {
        if (e.target.closest('a')) {
            return;
        }

        this.classList.toggle('active');

        mobileProductCards.forEach(otherCard => {
            if (otherCard !== this) {
                otherCard.classList.remove('active');
            }
        });
    });
});
