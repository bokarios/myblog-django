$(document).ready(function(){

    $('#comment-btn').click(function(){
        console.log('*Info: Assigning vars...')
        comment = $('#user-comment').val()
        user_id = $('#user-id').val()
        article_id = $('#article-id').val()
        csrf_token = $('[name="csrfmiddlewaretoken"]').val()

        console.log('Article: '+ article_id)
        console.log('Author: '+ user_id)
        console.log('Comment: '+ comment)
        console.log('csrf_token: '+ csrf_token)
        console.log('*Info: Passing vars to ajax func...')

        $.ajax({
			url: '/user/comment/',
			method: 'POST',
			data: { comment: comment, user_id: user_id, article_id: article_id, csrfmiddlewaretoken: csrf_token },
			success: function(data) {
				$('#comment-feedback').html(data)
				$('#user-comment').val('')
				$('#add-bus-feedback .alert').fadeOut(5000)
			},
			error: function(data) {
				$('#comment-feedback').html(
					'<p class="alert alert-warning text-center"> حصل خطأ ما </p>'
				)
				$('#comment-feedback .alert').fadeOut(5000)
			}
		})
    })

    btn_like = $('[name="like-btn"]')
    btn_like.click(function(){
        id = $(this).data('id')
        rd = $(this).data('rdr')
        user_id = $('#user-id').val()
        article_id = id
        csrf_token = $('[name="csrfmiddlewaretoken"]').val()

        $.ajax({
			url: '/user/like/',
			method: 'POST',
			data: { user_id: user_id, article_id: article_id, csrfmiddlewaretoken: csrf_token },
			success: function(data) {
                result = JSON.parse(data)
                if(result.success == '200') {
                    url = window.location.href
                    url = document.createElement('a')
                    // url = url+'#'+rd
                    top.location.href = url
                }
            },
			error: function(data) {
                console.log('*Warning: Bad request...')
            }
		})
    })

    btn_dislike = $('[name="dislike-btn"]')
    btn_dislike.click(function(){
        id = $(this).data('id')
        rd = $(this).data('rdr')
        user_id = $('#user-id').val()
        article_id = id
        csrf_token = $('[name="csrfmiddlewaretoken"]').val()

        $.ajax({
			url: '/user/dislike/',
			method: 'POST',
			data: { user_id: user_id, article_id: article_id, csrfmiddlewaretoken: csrf_token },
			success: function(data) {
                result = JSON.parse(data)
                if(result.success == '200') {
                    url = window.location.href
                    url = document.createElement('a')
                    // url = url+'#'+rd
                    top.location.href = url
                }
            },
			error: function(data) {}
		})
    })
})
