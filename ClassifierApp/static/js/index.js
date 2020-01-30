jQuery.ajaxSettings.traditional = true; 
$(function () {
    // turn off autocomplete
    $('input').attr('autocomplete','off');
    // create classes input UI
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
                'class': 'form-control input-class',
                'id': 'input-Class' + i,
                'placeholder': 'Class ' + i,
                'autocomplete':'off'
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
        var noti = $('#newdata-noti');
        var btnSubmit = $('#btn-newdata-submit');
        noti.html('');
        if (isInputBlank()===true) {
            noti.html('You must fill in all inputs !!!');
        }
        else {
            btnSubmit.prop('disabled', true);
            img_classes = []
            $('.input-class').each(function(){
                img_classes.push($(this).val());
                console.log($(this).val());
            })
            console.log(img_classes);
            $.ajax({
                type: "POST",
                url: url,
                data: {
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                    'dataset_name': $('#input-DatasetName').val(),
                    'num_classes': $('#input-NoOfClasses').val(),
                    'img_classes': img_classes
                },
                success: function (data) {
                    console.log(data);
                    btnSubmit.prop('disabled', false);
                    result = data['status']
                    switch(result){
                        case 'successful':{
                            noti.html('Finished collecting images!!!');
                            break;
                        }
                        case 'failed':{
                            noti.html('Failed to collect images!!!');
                            break;
                        }
                        case 'pending':{
                            noti.html('Waiting for uncompleted task!!!');
                        }
                    }  
                },
                error: function (data) {
                    console.log('An error occurred.');
                    console.log(data);
                    btnSubmit.prop('disabled', false);
                },
            });
        }
    })
})