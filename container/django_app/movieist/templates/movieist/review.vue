{% load static %}
<!DOCTYPE html>
<html lang="ja">

<head>
    <meta charset="UTF-8">
    <title>{{page_title}}</title>
    <link rel="stylesheet" type="text/css" href="{% static 'movieist/css/style.css' %}" />
    <script src="https://cdn.jsdelivr.net/npm/vue@2.6.12"></script>
    <script src="https://unpkg.com/vue-star-rating@1.7.0/dist/VueStarRating.umd.min.js"></script>
</head>

<body>
    <div class="header">
        <div class="header-title">
            <h3>Movieist</h3>
        </div>
        <div class="header-list">
            <ul>
                <li>注目の映画</li>
                <li>映画を探す</li>
                <li>レビュアーランキング</li>
                <li>レビューする</li>
            </ul>
        </div>
        <div class="header-menu">
            <img src="" alt="">
        </div>
    </div>

    <div class="main">
        <div class="container">
            <h1>{{title}}</h1>
            <div id="app">
                <h2>basic</h2>
                <star-rating></star-rating>
            </div>
            <table>
                <form action="{% url 'review' movie %}" method="post">
                    {% csrf_token %}
                    {{form}}
                    <tr>
                        <td></td>
                        <td><input type="submit" value="送信"></td>
                    </tr>
                </form>
            </table>
        </div>
    </div>

    <div class="footer">
        <div class="footer-container">
            <div class="footer-title">
                <h3>Movieist></h3>
                <p>投稿者のおすすめから見つける映画情報サイト >>></p>
            </div>
            <div class="footer-sitemap">
                <ul>
                    <li>/homePage</li>
                    <li>/search</li>
                    <li>/reviewerRanking</li>
                    <li>/overview</li>
                </ul>
                <ul>
                    <li>/login</li>
                    <li>/sign up</li>
                    <li>/profile</li>
                </ul>
            </div>
        </div>
    </div>
    <script>
        Vue.component('star-rating', VueStarRating.default)

        new Vue({
            el: '#app',
            methods: {
                setRating: function (rating) {
                    this.rating = "You have Selected: " + rating + " stars";
                },
                showCurrentRating: function (rating) {
                    this.currentRating = (rating === 0) ? this.currentSelectedRating : "Click to select " + rating + " stars"
                },
                setCurrentSelectedRating: function (rating) {
                    this.currentSelectedRating = "You have Selected: " + rating + " stars";
                }
            },
            data: {
                rating: "No Rating Selected",
                currentRating: "No Rating",
                currentSelectedRating: "No Current Rating",
                boundRating: 3,
            }
        });
    </script>
</body>

</html>