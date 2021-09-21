addEventListener('DOMContentLoaded', () => {
    const btnMenu = document.querySelector('.btn-menu')
    if (btnMenu) {
        btnMenu.addEventListener('click', () => {
            const menuList = document.querySelector('.menu-items')
            menuList.classList.toggle('show')
        })
    }
})

window.onload = () => {
    const menuItems = document.getElementById('menu-items')
    const menuItemss = document.getElementById('menu-items').children
    for(let i=0; i < menuItemss.length;i++){
        menuItemss[i].addEventListener('click', (e) =>{
            const item = menuItemss[i]
            removeActive(menuItems, item)
            
        })
    }

    const removeActive = (menuItems, item) => {
        Array.from(menuItems.children).forEach(x => x.classList.remove('active'))
        item.classList.add('active')
    }
}