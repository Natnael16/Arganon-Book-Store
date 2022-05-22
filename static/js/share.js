Share = {
    facebook: function(purl) {
        url = 'http://www.facebook.com/sharer.php?u=';
        url += 'http://127.0.0.1:8000/book_detail/' + encodeURIComponent(purl);
        Share.popup(url);
    },
    twitter: function(purl) {

        url = 'http://twitter.com/share?url=';
        url += 'http://127.0.0.1:8000/book_detail/' + encodeURIComponent(purl);
        url += '&text=Check out this book';

        Share.popup(url);
    },
    telegram: function(purl) {
        url = 'https://t.me/share/url?url=';
        url += 'http://127.0.0.1:8000/book_detail/' + encodeURIComponent(purl);
        url += '&text=Check out this book';
        Share.popup(url);
    },
    instagram: function(purl) {
        url = 'https://t.me/share/url?url=';
        url += 'http://127.0.0.1:8000/book_detail/' + encodeURIComponent(purl);
        url += '&text=Check out this book';
        Share.popup(url);
    },

    popup: function(url) {
        window.open(url, '', 'toolbar=0,status=0,width=626, height=436');
    }
};