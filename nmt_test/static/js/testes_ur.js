$(document).ready(function() {
    $('.btn-save-test').click(function() {
        var tema_test_id = 1;  // Опціонально, ви можете отримати значення зі сторінки
        var test_id = $(this).data('test-id');
        var an = $(this).data('an');

        $.ajax({
            type: 'POST',
            url: '/testes_ur/' + tema_test_id + '/' + test_id + '/' + an + '/',
            success: function(response) {
                console.log(response);
                // Обробка відповіді
            },
            error: function(error) {
                console.error(error);
                // Обробка помилок
            }
        });
    });
});
