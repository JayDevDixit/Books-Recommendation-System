let all_books = document.getElementsByClassName('card')
let x,y
for(let book of all_books)
book.addEventListener('click',sent)
function sent(event){
    x = event.target.parentElement
    x = x.getElementsByTagName('h1')[0]
    book_name = x.innerHTML
    console.log('Book-Name = ',book_name)

    y = event.target.parentElement
    y = y.nextElementSibling
    y.value = book_name
    console.log(y.nextElementSibling)
    y.nextElementSibling.click()
}