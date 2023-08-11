
const un_block = document.querySelectorAll(".block-unblock-action")
console.log(un_block)

un_block.forEach((btn) =>{
    btn.addEventListener('click', (e) => {
        console.log("clicked")
        var form = btn.parentElement;
        var formData = new FormData(form);
        var ajaxUrl = form.getAttribute('data-url');
        var username = form.getAttribute('data-username');
        console.log(form,formData,username,ajaxUrl)

        formData.append('username', username);
        formData.append('btn', btn.getAttribute("name"));
        var xhr = new XMLHttpRequest();

        xhr.open('POST', ajaxUrl, true);
        // xhr.setRequestHeader('X-CSRFToken', csrfToken); 
        xhr.onreadystatechange = (ev) => {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.msg==1){
                    btn.parentElement.parentElement.remove()
                }
                if (response.msg==2){
                    btn.parentElement.parentElement.remove()
                }

            }
           
        };
        xhr.send(formData);
    });  
});

