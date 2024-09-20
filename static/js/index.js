 // Hide flash messages after 5 seconds
 setTimeout(function() {
    const flashMessageContainer = document.getElementById('flash-messages');
    if (flashMessageContainer) {
        flashMessageContainer.style.transition = 'opacity 0.5s ease';
        flashMessageContainer.style.opacity = '0';
        setTimeout(() => flashMessageContainer.remove(), 500); // Remove after fading out
    }
}, 5000); // 5 seconds delay before fading out