document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.reply-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const commentId = btn.dataset.commentId;
            const form = document.getElementById(`reply-form-${commentId}`);
            if (form) {
                form.style.display = form.style.display === 'block' ? 'none' : 'block';
            }
        });
    });
});