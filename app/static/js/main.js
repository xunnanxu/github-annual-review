(function () {
    var apiUrl = '/review'

    $(document).ready(function () {
        function fillBlanks (data) {
            $('.userDisplayName').text(data.user.name);
            $('#firstRepoName').text(data.first_repo_name);
            $('#daysInGithub').text(data.user.days_since);
            $('#daysSinceFirstRepo').text(data.user.days_since_first_repo);
            if (!data.favorite_repo && !data.favorite_3p_repo) {
                $('#favRepoPage').remove();
            } else {
                if (!data.favorite_repo) {
                    $('#favRepoSection').remove();
                    $('#noFavRepo').removeClass('hidden');
                } else {
                    $('#favoriteRepo').text(data.favorite_repo.repo);
                    if (!data.favorite_repo.commits) {
                        $('#showCommitsFavRepo').hide();
                    }
                    $('#commitsFavRepo').text(data.favorite_repo.commits);
                    if (!data.favorite_repo.issues) {
                        $('#showIssuesFavRepo').hide();
                    }
                    $('#issuesFavRepo').text(data.favorite_repo.issues);
                    if (!data.favorite_repo.prs) {
                        $('#showPRsFavRepo').hide();
                    }
                    $('#prsFavRepo').text(data.favorite_repo.prs);
                }
                if (!data.favorite_3p_repo) {
                    $('#fav3PRepoSection').remove();
                }
                else {
                    $('#favorite3PRepo').text(data.favorite_3p_repo.repo);
                    if (!data.favorite_3p_repo.commits) {
                        $('#showCommitsFav3PRepo').hide();
                    }
                    $('#commitsFav3PRepo').text(data.favorite_3p_repo.commits);
                    if (!data.favorite_3p_repo.issues) {
                        $('#showIssuesFav3PRepo').hide();
                    }
                    $('#issuesFav3PRepo').text(data.favorite_3p_repo.issues);
                    if (!data.favorite_3p_repo.prs) {
                        $('#showPRsFav3PRepo').hide();
                    }
                    $('#prsFav3PRepo').text(data.favorite_3p_repo.prs);
                }
            }
            if (data.most_liked_repo) {
                $('#mostLikedRepo').text(data.most_liked_repo.repo);
                $('#likedRepoStars').text(data.most_liked_repo.stars);
                $('#likedRepoForks').text(data.most_liked_repo.forks);
            } else {
                $('#mostLikedRepoPage').remove();
            }
            $('#totalCommits').text(data.total_commits);
            $('#linesChanged').text(data.total_lines_committed);
            $('#totalIssues').text(data.total_issues);
            if (data.language_scores && data.language_scores.length > 0) {
                $('#favLanguage').text(data.language_scores[0][0])
            } else {
                $('#favLanguagePage').remove();
            }
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
            },
            error: function (xhr) {
                $('#loader').hide();
                $('#error').text('Error: ' + xhr.responseJSON.message).removeClass('hidden');
            },
        })
    })
})();