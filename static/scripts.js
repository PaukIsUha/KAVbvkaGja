$(document).ready(function() {
    $('.comment-button').click(function() {
        if ($(this).hasClass('disabled')) {
            return;
        }
        var dataId = $(this).data('id');
        var comment = $(this).data('comment');
        $('#data_id').val(dataId);
        $('#comment').val(comment);
        $('#commentModal').show();
        });

        $('#closeModal').click(function() {
                $('#commentModal').hide();
        });

        // Для комментариев PC
        $('.comment-pc-button').click(function() {
            if ($(this).hasClass('disabled')) {
                return;
            }
            var dataId = $(this).data('id');
            var commentPc = $(this).data('comment-pc');
            $('#dataPc_id').val(dataId);
            $('#comment_pc').val(commentPc);
            $('#commentPcModal').show();
        });

        $('#closePcModal').click(function() {
            $('#commentPcModal').hide();
        });
});
