(function () {
    function getCookie(name) {
        var v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
        return v ? v[2] : null;
    }

    var apiUrl = '/review'
    var accessToken = getCookie('gh_access_token');
    if (!accessToken) {
        var urlParams = new URLSearchParams(window.location.search.substring(1));
        var code = urlParams.get('code');
        if (!code) {
            $('#loaderMessage').html('Access token not found.<br>Redirecting to Github to authorize...')
            window.setTimeout(function () {
                window.location.href = '/login';
            }, 1000);
            return;
        }
        apiUrl += '?code=' + code
    }

    $(document).ready(function () {
        function fillBlanks (data) {
            $('.userDisplayName').text(data.user.name);
            $('#firstRepoName').text(data.first_repo_name);
            $('#daysInGithub').text(data.user.days_since);
            $('#daysSinceFirstRepo').text(data.user.days_since_first_repo);
            $('#favoriteRepo').text(data.favorite_repo.repo);
            $('#commitsFavRepo').text(data.favorite_repo.commits);
            $('#issuesFavRepo').text(data.favorite_repo.issues);
            $('#favorite3PRepo').text(data.favorite_3p_repo.repo);
            $('#commitsFav3PRepo').text(data.favorite_3p_repo.commits);
            $('#issuesFav3PRepo').text(data.favorite_3p_repo.issues);
            $('#mostLikedRepo').text(data.most_liked_repo.repo);
            $('#likedRepoStars').text(data.most_liked_repo.stars);
            $('#likedRepoForks').text(data.most_liked_repo.forks);
            $('#totalCommits').text(data.total_commits);
            $('#linesChanged').text(data.total_lines_committed);
            $('#totalIssues').text(data.total_issues);
            $('#favLanguage').text(data.language_scores[0][0])
        }
    
        $.ajax(apiUrl, {
            dataType: 'json',
            success: function (data) {
                $('#loader').hide()
                $('.swiper-container').removeClass('hidden');
                fillBlanks(data);
            
                var mySwiper = new Swiper ('.swiper-container', {
                    direction: 'vertical',
                    pagination: {
                        el: '.swiper-pagination',
                        clickable: true,
                    },
            
                    on:{
                        init: function () {
                            swiperAnimateCache(this);
                            swiperAnimate(this);
                        }, 
                        slideChangeTransitionEnd: function () { 
                            swiperAnimate(this);
                        }
                    }
                })
            }
        })
    })
})();