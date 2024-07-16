// Assurez-vous d'inclure jQuery dans votre projet si vous utilisez jQuery
$(document).ready(function() {
    // Lorsque l'utilisateur clique sur un chat dans la liste
    $('.person').click(function() {
        var chatId = $(this).data('chat-id'); // Récupère l'ID du chat à partir de l'attribut data

        // Effectue une requête AJAX pour récupérer les détails du chat
        $.ajax({
            url: '/chat/' + chatId + '/', // URL du détail du chat dans votre application Django
            type: 'GET',
            dataType: 'html',
            success: function(data) {
                $('.right').html(data); // Remplace le contenu de la colonne de droite par les détails du chat
            },
            error: function(xhr, status, error) {
                console.error('Error fetching chat details:', error);
            }
        });
    });
});
