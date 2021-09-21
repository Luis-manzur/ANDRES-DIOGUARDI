window.onload = () => {
    const bigPhoto = document.getElementById('big-photo')
    const photoGalery = document.getElementById('photo-galery').children
    for(let i=0; i < photoGalery.length;i++){
        photoGalery[i].addEventListener('click', (e) =>{
            const nweSrc= photoGalery[i].getAttribute("src")
            bigPhoto.setAttribute("src", nweSrc)
        })
    }
}