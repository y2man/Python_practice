class Book: 

    def __init__(self,book_id,title,author):
        self.available = True
        self.book_id = book_id
        self.title = title
        self.author = author
    def display_info(self):
        
        print(self.book_id)
        print(self.title)
        print(self.author)
        print(self.available)
        
class Library:    

    
    def __init__(self):
        
        self.books = []

    def add_books(self,book):
        self.books.append(book)        

    def display_books(self):
        
        for book in self.books:
             book.display_info()
    
    def borrow_book(self,book_id):
        
        for book in self.books:
        
            if book.book_id==book_id and book.available==True:
                print(" You can borrow the book")
                book.available =False
            
            elif book.book_id==book_id and book.available ==False:
                
                print("The book isn't available right now!")   
                
            
            else:
                print("Book is not found!")
        
        
            
        
        
book1 = Book(1,"The Great Gatsby","f. Scott Fitzgerald")
book2= Book(2,"to kill a mockingbird", "Harper lee")

library1 = Library()
library1.add_books(book1)
library1.add_books(book2)
library1.display_books()
library1.borrow_book(1)   # Borrow successfully
library1.borrow_book(1)   # Already borrowed
library1.borrow_book(99)  # Book not found



