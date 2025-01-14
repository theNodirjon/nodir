document.addEventListener('DOMContentLoaded', function() {
    // Add to cart toggle button
    const addToCartBtn = document.querySelector('.add-to-cart');
    addToCartBtn.addEventListener('click', function() {
        if (this.classList.contains('btn-success')) {
            this.classList.remove('btn-success');
            this.textContent = 'Add to Cart';
        }
    });

    // Review form submission animation
    const reviewForm = document.getElementById('new-review-form');
    reviewForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Formani to'xtatamiz, lekin AJAX orqali yuboramiz

        const submitBtn = this.querySelector('button[type="submit"]');
        submitBtn.textContent = 'Submitting...';
        submitBtn.disabled = true;

        const formData = new FormData(this); // Form ma'lumotlarini olamiz

        fetch(window.location.href, { // Hozirgi URLga so'rov yuboriladi
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: formData
        })
        .then(response => {
            if (response.ok) {
                submitBtn.textContent = 'Submitted!';
                submitBtn.classList.add('btn-success');
                setTimeout(() => {
                    submitBtn.textContent = 'Submit Review';
                    submitBtn.classList.remove('btn-success');
                    submitBtn.disabled = false;
                    reviewForm.reset();
                    location.reload(); // Sahifani qayta yuklash (kerak bo'lsa)
                }, 2000);
            } else {
                throw new Error('Something went wrong');
            }
        })
        .catch(error => {
            console.error(error);
            alert('An error occurred while submitting the review.');
            submitBtn.textContent = 'Submit Review';
            submitBtn.disabled = false;
        });
    });
});
