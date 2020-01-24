$(function () {
    $('#input-NoOfClasses').change(function () {
        n = $(this).val();
        group_NoOfClasses = $('#group-NoOfClasses');
        $('.group-classes').remove();
        for (i = n; i >= 1; --i) {
            formgroup_div = $('<div>', {
                'class': 'form-group group-classes',
            });
            text_label = 'Class ' + i + ': ';
            $('<label>', { 'class': "control-label col-sm-4", 'text': text_label }).appendTo(formgroup_div);
            $('<div>', { 'class': 'col-sm-8' }).append($('<input>', {
                'type': 'text',
                'class': 'form-control',
                'id': 'input-Class' + i,
                'placeholder': 'Class ' + i
            })).appendTo(formgroup_div)
            group_NoOfClasses.after(formgroup_div)
        }
    })
    function isInputBlank() {
        res = false;
        $('#form-newdata input').each(function () {
            if ($(this).val() ===  '') {
                res = true;
                return false;
            }
        })
        return res;
    }
    $('#form-newdata').submit(function (e) {
        e.preventDefault(); // avoid to execute the actual submit of the form.
        var form = $(this);
        var url = form.attr('action');
        var noti = $('#newdata-noti')
        noti.html('');
        if (isInputBlank()===true) {
            noti.html('You must fill in all inputs !!!');
        }
        else {
            $.ajax({
                type: "POST",
                url: url,
                data: form.serialize(), // serializes the form's elements.
                success: function (data) {
                    console.log(data) // show response from the php script.
                },
                error: function (data) {
                    console.log('An error occurred.');
                    console.log(data);
                },
            });
        }
    })
})