const story2Html = story => {
    return `
        <div>
            <img src="${ story.user.thumb_url }" class="pic" alt="profile pic for ${ story.user.username }" />
            <p>${ story.user.username }</p>
        </div>
    `;
};

// fetch data from your API endpoint:
const displayStories = () => {
    fetch('/api/stories')
        .then(response => response.json())
        .then(stories => {
            const html = stories.map(story2Html).join('\n');
            document.querySelector('.stories').innerHTML = html;
        })
};

const destroyModal = ev => {
    document.querySelector('#modal-container').innerHTML = "";
};

const showPostDetail = ev => {
    const postId = ev.currentTarget.dataset.postId;
    fetch(`/api/posts/${postId}`)
        .then(response => response.json())
        .then(post => {
            const html = `
                <div class="modal-bg">
                    <button onclick="destroyModal(event)">Close</button>
                    <div class="modal">
                        <img src="${post.image_url}" />
                    </div>
                </div>`;
            // var x = document.createElement("div");
            // x.innerHTML = html;
            // document.body.appendChild(x.firstElementChild)
            document.querySelector('#modal-container').innerHTML = html;
        })
};

const displayComments = (comments, postID) => {
    let html = '';
    if (comments.length > 1) {
        html += `
            <button class="link" data-post-id="${postID}" onclick="showPostDetail(event);">
                view all ${comments.length} comments
            </button>
        `;
    }
    if (comments && comments.length > 0) {
        const lastComment = comments[comments.length - 1];
        html += `
            <p>
                <strong>${lastComment.user.username}</strong> 
                ${lastComment.text}
            </p>
            <div>${lastComment.display_time}</div>
        `
    }
    html += `
        <div class="add-comment">
            <div class="input-holder">
                <input type="text" id="comment-${postID}" aria-label="Add a comment" placeholder="Add a comment...">                       
            </div>
            <button onclick="addComment(event, ${postID})" class="link">Post
            </button>
        </div>
    `;
    return html;
};



const addComment = (ev, postId) => {
    const elem = ev.currentTarget;
    const comments = document.querySelector(`#comment-${postId}`).value;
    if (comments == '')
    {
        return;
    }
    fetch(`/api/comments/`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ "post_id": postId, "text": comments })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        updatePost(postId);
    });
    
};
/*
<section class="card">
        Already done
       
        <div class="caption">
            <p>
                <strong>{{ post.get('user').get('username') }}</strong> 
                {{ post.title }}.. <button class="link">more</button>
            </p>
        </div>
        <div class="comments">
            {% if post.get('comments')|length > 1 %}
                <p><button class="link">View all {{ post.get('comments')|length }} comments</button></p>
            {% endif %}
            {% for comment in post.get('comments')[:1] %}
                <p>
                    <strong>{{ comment.get('user').get('username') }}</strong> 
                    {{ comment.get('text') }}
                </p>
            {% endfor %}
            <p class="timestamp">{{ post.get('display_time') }}</p>
        </div>
    </div>
    <div class="add-comment">
        <div class="input-holder">
            <input type="text" aria-label="Add a comment" placeholder="Add a comment...">
        </div>
        <button class="link">Post</button>
    </div>
</section>

*/
const updatePost = postId => {
    fetch(`/api/posts/${postId}`)
        .then(response=>response.json())
        .then(post=>{
            console.log(post)
            console.log(post2Html(post))
            document.getElementById(post.id).innerHTML=post2Html(post);
        })
}
const likeUnlike = ev => {
    const elem = ev.currentTarget;
    const likeId = elem.dataset.likeId;
    const postId = elem.dataset.postId;

    if(elem.getAttribute("aria-checked") === "false") {
        like(postId);
    } else {
        unlike(likeId,postId);
    }
};

const like = postId => {
    console.log('like', postId);
    fetch(`/api/posts/${postId}/likes/`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ "post_id": postId })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        updatePost(postId);
    });
};

const unlike = (likeId, postId) => {
    console.log('unlike', likeId, postId);
    fetch(`/api/posts/${ postId }/likes/${likeId}`,{
        method: "DELETE"
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        updatePost(postId);
    });
};

const post2Html = post => {
    return `
        <section id="${post.id}" class="card"> 
            <div class="header">
                <h3>${ post.user.username }</h3>
                <i class="fa fa-dots"></i>
            </div>
            <img src="${ post.image_url }" alt="Image posted by ${ post.user.username }" width="300" height="300">
            <div class="info">
                <div class="buttons">
                    <div>
                        <button 
                            ${ post.current_user_like_id ? 'aria-checked="true"' : 'aria-checked="false"' } 
                            onclick="likeUnlike(event)"
                            data-post-id="${post.id}"
                            ${ post.current_user_like_id ? `data-like-id="${post.current_user_like_id}"` : '' } >
                            <i class="fa${ post.current_user_like_id ? 's' : 'r' } fa-heart"></i>
                        </button>
                        <i class="far fa-comment"></i>
                        <i class="far fa-paper-plane"></i>
                    </div>
                    <div>
                        <button 
                            ${ post.current_user_bookmark_id? 'aria-checked="true"' : 'aria-checked="false"' } 
                            onclick="toggleBookmark(event)"
                            data-post-id="${post.id}"
                            ${  post.current_user_bookmark_id? `data-bookmark-id="${post.current_user_bookmark_id}"` : '' } >
                            <i class="fa${ post.current_user_bookmark_id ? 's' : 'r' } fa-bookmark"></i>
                        </button>
                    </div>
                </div>
                <p class="likes"><strong>${ post.likes.length } like${post.likes.length != 1 ? 's' : ''}</strong></p>

                <div class="caption">
                <p>
                    <strong>${ post.user.username }</strong> 
                    ${ post.caption }
                </p>
            </div>
            <div class="comments">
                ${ displayComments(post.comments, post.id) }
            </div>
        </section>
    `;
};

// fetch data from your API endpoint:
const displayPosts = () => {
    fetch('/api/posts')
        .then(response => response.json())
        .then(posts => {
            const html = posts.map(post2Html).join('\n');
            document.querySelector('#posts').innerHTML = html;
        })
};


// 1. Get the post data from the API endpoint (/api/posts?limit=10)
// 2. When that data arrives, we're going to build a bunch of HTML cards (i.e. a big string).
// 3. Update the container and put the html on the inside of it.


//SUGGESTIONS

const suggestions2Html = user => {
    return `
        <section>
            <img src="${user.thumb_url}" class="pic" alt="Profile pic for ${user.username}" />
            <div>
                <p>${user.username}</p>
                <p>suggessted for you</p>
            </div>
            <div>
                <button
                    class="link following"
                    id="follow-${ user.id }"
                    data-username="${ user.username }"
                    data-user-id="${ user.id }"
                    aria-checked="false"
                    aria-label="Follow ${ user.username }"
                    onclick="toggleFollow(event)">follow
                </button>
            </div>
        </section>`;
};

const displaySuggestions = () => {
    fetch('/api/suggestions')
        .then(response => response.json())
        .then(suggestedUsers => {
           document.querySelector('.suggestions').innerHTML = suggestedUsers.map(suggestions2Html).join('\n');
        })
};

const toggleFollow = ev => {
    const elem = ev.currentTarget;
    const userId = elem.dataset.userId;
    if(elem.getAttribute('aria-checked').trim() === 'false') {
        follow(userId);
    } else {
        const followingId =elem.dataset.followingId;
        unfollow(followingId,userId);
    }
};

const follow = userId => {
    console.log('follow', userId);
    fetch('/api/following/', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ "user_id": userId })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        const elem = document.querySelector(`#follow-${ data.following.id}`);
        elem.innerHTML = "unfollow";
        elem.classList.add('active');
        elem.setAttribute('aria-checked', 'true');
        elem.setAttribute('aria-label', "Unfollow " + elem.dataset.username);
        elem.setAttribute('data-following-id', data.id);
    });
};

const unfollow = (followingId, userId) => {
    console.log('unfollow', followingId, userId);
    fetch(`/api/following/${ followingId }`,{
        method: "DELETE"
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        const elem = document.querySelector(`#follow-${ userId}`);
        elem.innerHTML = "follow";
        elem.classList.remove('active');
        elem.setAttribute('aria-checked', 'false');
        elem.setAttribute('aria-label', "Follow " + elem.dataset.username);
        elem.removeAttribute('data-following-id', data.id);
    });
};



const toggleBookmark = ev => {
    const elem = ev.currentTarget;
    const bookmarkId = elem.dataset.bookmarkId;
    const postId = elem.dataset.postId;
    console.log(bookmarkId)
    if(bookmarkId) {
        unBookmarked(bookmarkId, postId);
        
    } else {
        Bookmarked(postId);
    }
};

const Bookmarked = postId => {
    console.log('bookmarked', postId);
    fetch('/api/bookmarks/', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ "post_id": postId })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        updatePost(postId);
    });
};

const unBookmarked = (bookmarkId, postId) => {
    console.log('unbookmarked', bookmarkId, postId);
    fetch(`/api/bookmarks/${ bookmarkId }`,{
        method: "DELETE"
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        updatePost(postId);
    });
};



const initPage = () => {
    displayStories();
    displayPosts();
    displaySuggestions();
};

// invoke init page to display stories:
initPage();