
const react = document.querySelectorAll(".btn-reaction")
console.log(react)

react.forEach((btn) =>{
    btn.addEventListener('click', (e) => {
        console.log("clicked")
        var form = btn.parentElement;
        var formData = new FormData(form);
        var ajaxUrl = form.getAttribute('url-data');
        var type = btn.getAttribute('name');

        formData.append( "type", String(type)  );
        
        
        fetch(ajaxUrl,
        {
            method: "POST",
            body: formData
        })
        .then((res) => res.json() )
        .then((data) => { 
            console.log(data)
            if (data.msg==1){
                btn.classList.add("btn-outline-secondary")
                btn.classList.remove("btn-outline-primary")
                counter = btn.querySelector(".counter")
                counter.innerText = Number(counter.innerText)-1
                console.log("donne 1")
            }
            else if (data.msg==2 || data.msg==5){
                btn.classList.add("btn-outline-primary")
                btn.classList.remove("btn-outline-secondary")
                counter = btn.querySelector(".counter")
                counter.innerText = Number(counter.innerText)+1

                dislike = form.querySelector(`[name="${data.msg==2?"dislikebtn":"likebtn"}"]`)
                dislike.classList.remove("btn-outline-primary")
                dislike.classList.add("btn-outline-secondary")
                counter = dislike.querySelector(".counter")
                counter.innerText = Number(counter.innerText)-1

                console.log("donne 2")
            }
            else if (data.msg==3){
                btn.classList.add("btn-outline-primary")
                btn.classList.remove("btn-outline-secondary")
                counter = btn.querySelector(".counter")
                counter.innerText = Number(counter.innerText)+1
                console.log("donne 3")
            }

 
         });






    });  
});

