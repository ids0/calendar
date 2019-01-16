function addPage(name)
{
    if(name == "")
        return;

    var ajax = new XMLHttpRequest();

    ajax.onreadystatechange = function() {
        if (ajax.readyState == 4 && ajax.status == 200) {
            $('#infodiv').html(ajax.responseText);
        }
    };



    ajax.open('GET', 'add_'+ name, true)
    ajax.send();

};
