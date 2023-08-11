
const buttons = document.querySelectorAll(".requests-button")


console.log(buttons)



buttons.forEach((btn) =>{
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
                if (response.msg==0){
                    console.log("something went wrong")
                }
                else if (response.msg==1){
                    btn.parentElement.parentElement.remove()
                    console.log("confirmed")
                }
                else if (response.msg==2){
                    btn.parentElement.parentElement.remove()
                    console.log("ignored")
                }

            }
           
        };
        xhr.send(formData);
        console.log("sent")
    });  
});

