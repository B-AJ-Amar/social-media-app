
const follow = document.querySelectorAll(".follow-button")
console.log(follow)

follow.forEach((btn) =>{
    btn.addEventListener('click', (e) => {
        console.log("clicked")
        var form = btn.parentElement;
        var formData = new FormData(form);
        // var csrfToken = form.getAttribute('data-csrf-token');
        var ajaxUrl = form.getAttribute('data-url');
        var username = form.getAttribute('data-username');
        console.log(form,formData,username,ajaxUrl)

        formData.append('username', username);
        var xhr = new XMLHttpRequest();

        
        xhr.open('POST', ajaxUrl, true);
        // xhr.setRequestHeader('X-CSRFToken', csrfToken); 
        xhr.onreadystatechange = (ev) => {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.msg==1){
                    btn.classList.remove("btn-success")
                    btn.classList.add("btn-outline-danger")
                    btn.textContent = "Unfollow"
                    console.log("donne 1")

                }
                if (response.msg==2){
                    btn.classList.add("btn-success")
                    btn.classList.remove("btn-outline-danger")
                    btn.textContent = "Follow"
                    console.log("donne 2")

                }
                if (response.msg==3){
                    btn.classList.add("btn-outline-success")
                    btn.classList.remove("btn-success")
                    btn.textContent = "Requested"
                    console.log("donne 3")

                }
                if (response.msg==4){
                    btn.classList.add("btn-success")
                    btn.classList.remove("btn-outline-success")
                    btn.textContent = "Follow"
                    console.log("donne 4")

                }

            }
           
        };
        xhr.send(formData);
    });  
});

