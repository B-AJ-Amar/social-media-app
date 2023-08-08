const UsersBtn = document.querySelector(".search-results-btn-users")
const PostsBtn = document.querySelector(".search-results-btn-posts")

const UsersContainer = document.querySelector(".search-results-container-users")
const PostsContainer = document.querySelector(".search-results-container-posts")

UsersBtn.addEventListener("click",(e) =>{
    if (!UsersBtn.classList.contains("active")){
        UsersBtn.classList.add("active");
        PostsBtn.classList.remove("active");

        UsersContainer.style.display = "flex";
        PostsContainer.style.display = "none";

    }
})

PostsBtn.addEventListener("click",(e) =>{
    if (!PostsBtn.classList.contains("active")){
        UsersBtn.classList.remove("active");
        PostsBtn.classList.add("active");

        UsersContainer.style.display = "none";
        PostsContainer.style.display = "block";

    }
})