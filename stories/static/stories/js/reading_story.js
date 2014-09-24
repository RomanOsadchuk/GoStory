function init_story_reading(jQuery) {

    var lastChapPk = $('#story div.chapter-single').last().data('chapterPk');
    $('.continuation-chapter-form #id_parent').val(lastChapPk);
    
    $('.suggest-continuation').off('click').on('click', function(e){
        e.preventDefault();
        $('.continuation-chapter-form').toggle('fast');
    });
    
    $('.suggest-chapter').off('click').on('click', function(e){
        e.preventDefault();
        $(this).closest('.chapter-single').find('.alternative-chapter-form').toggle('fast');
    });
    
    $('.chapter-link').off('click').on('click', function(e){
        e.preventDefault();
        var link = $(this),
            chapterType = $(this).data('chapterType'),
            chapter = $(this).closest('.chapter-single');
        // disable chapters clicking
        $.get(this.href).done(function(data){            
            if (chapterType === 'parent') {
                $('#story').prepend(data);
                $('#story').children('.chapter-children').first().remove();
                var parentPk = $('#story div').first().data('parentPk');
                if (parentPk) link.attr('href', '/ajax/chapter/' + parentPk);
                else link.remove();
            }
            else {
                chapter.nextAll('.chapter-single').remove();
                $('.chapter-children').remove();
                if (chapterType === 'neighbour') chapter.remove();
                $('#story').append(data);
            }
            init_story_reading();
            init_common();
        }).fail(function(response){
            alert('smth wrong');
        }).always(function(){
            // enable clicking
        });
    });
    
    $('.add-chapter-form').off('submit').on('submit', function(e){
        e.preventDefault();
        var form = $(this),
            data = $(this).serializeArray(),
            chapter = $(this).closest('.chapter-single');
        $.post(this.action, data).done(function(response){
            if (chapter.html() !== undefined) {
                chapter.nextAll('.chapter-single').remove();
                chapter.remove();
            }
            form.trigger('reset');
            $('.continuation-chapter-form').hide();
            $('.chapter-children').remove();
            $('#story').append(response);
            init_story_reading();
            init_common();
        }).fail(function(response){
            var errors = $.parseJSON(response.responseJSON);
            $.each(errors, function(key, value) {
                form.find('.'+key+'-errors').html(value[0]['message']);
            });
        });
    });
}


$(document).ready(init_story_reading);

