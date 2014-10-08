function changeQueryStr(name, value) {
    var query = window.location.search.substring(1),
        newQuery = '?', notFound = true,
        vars = query.split('&');
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        if (pair == '' || pair[0] == 'page') continue;
        if (pair[0] == name) { notFound = false; pair[1] = value; }
        if (pair[1].length > 0) { newQuery += pair[0] + '=' + pair[1] + '&'; }
    }
    if (notFound && value.length > 0) { newQuery += name + '=' + value; }
    else if (newQuery.length == 1) { newQuery = ''; }
    else { newQuery = newQuery.slice(0,-1); }
    
    var loc = window.location,
        ajaxurl = '/ajax' + loc.pathname + newQuery,
        newurl = loc.protocol + "//" + loc.host + loc.pathname + newQuery;
    $.get(ajaxurl).done(function(data){
        $('#ajax-content').html(data);
        init_pagination();
    });
    window.history.pushState({path:newurl},'',newurl); 
}


function init_filtering_stories(jQuery) {
    $('#filtering input').change(function(){
        var input = $(this), name = input[0].name, value=input.val();
        changeQueryStr(name, value);
    });
}


function init_pagination(jQuery) {
    $('.pager a').on('click', function(e){
        e.preventDefault();
        var value = $(this).closest('li').data('pageNum');
        if (value) changeQueryStr('page', String(value));
    });
}


$(document).ready(init_filtering_stories);
$(document).ready(init_pagination);

