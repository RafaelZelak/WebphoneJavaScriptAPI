// scripts.js

document.addEventListener('DOMContentLoaded', () => {
    const togglePassword = document.querySelector('#toggle-password');
    const passwordField = document.querySelector('#password');
    const eyeIcon = document.querySelector('#eye-icon');

    togglePassword.addEventListener('click', () => {
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);
        eyeIcon.classList.toggle('text-gray-500');
        eyeIcon.classList.toggle('text-gray-300');
    });

    // Remove alert messages after 3 seconds with animation
    const alertContainer = document.querySelector('#alert-container');
    if (alertContainer) {
        setTimeout(() => {
            alertContainer.classList.add('opacity-0', 'transition-opacity');
            setTimeout(() => alertContainer.remove(), 500);
        }, 3000);
    }
});
