function init_chapter_feedback(jQuery) {
    $('.chapter-feedback').off('click').on('click', function(e){
        e.preventDefault();
        var link = $(this),
            feedbackType = $(this).data('feedbackType'),
            chapter = $(this).closest('.chapter-single');
        $.get(this.href, {feedback_type: feedbackType}).done(function(responce){           
            if (feedbackType === 'add-bookmark') {
                link.data('feedbackType', 'remove-bookmark');
                link.html('remove bookmark');
            }
            else if (feedbackType === 'remove-bookmark') {
                link.data('feedbackType', 'add-bookmark');
                link.html('add bookmark');
            }
            else if (feedbackType === 'like') {
                link.data('feedbackType', 'cancel-like');
                link.html('cancel');
                var newVal = parseInt(link.prev().html()) + 1;
                link.prev().html(newVal);
            }
            else if (feedbackType === 'cancel-like') {
                link.data('feedbackType', 'like');
                link.html('like it!');
                var newVal = parseInt(link.prev().html()) - 1;
                link.prev().html(newVal);
            }
        }).fail(function(response){
            alert('smth wrong');
        });
    });
}


$(document).ready(init_chapter_feedback);

