
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
        found=False
        for b in self.books:
            if(b.book_id==book.book_id):
                print("The book is already exist")
                found=True
                
                
        if not found:
         self.books.append(book)   
         print("The book is successfully added!")     

    def display_books(self):
        
        if not self.books:
            print("No books in the library.")
        else:
        
            for book in self.books:
                book.display_info()
    
    def borrow_book(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                if book.available:
                    book.available = False
                    print("You borrowed the book successfully!")
                else:
                    print("The book isn't available right now!")
                return

        print("Book not found!")
    def return_book(self, book_id):
       for book in self.books:
        if book.book_id == book_id:
            if not book.available:
                book.available = True
                print(f"Book {book_id} has been returned successfully!")
            else:
                print("This book is already available.")
            return

       print("Book not found in this library!")
       
    def search(self, title=None, author=None):
     for book in self.books:
        title_match = title is not None and title.lower() == book.title.lower()
        author_match = author is not None and author.lower() == book.author.lower()

        if title_match or author_match:
            print("We found the book:")
            book.display_info()
            return

     print("We can't find this book!")
    
    def count_books(self):
       book_numbers = len(self.books)
       Available_counter=0
       print(f"Total books: {book_numbers}") 
       
       for book in self.books:
           
           if book.available:
               Available_counter+=1
               
       print(f"Available books: {Available_counter}") 
       
       borrowed_books= book_numbers-Available_counter
       
       print(f"Borrowed books: {borrowed_books}") 

            
            
            
            
        
        
# book1 = Book(1,"The Great Gatsby","f. Scott Fitzgerald")
# book2= Book(2,"to kill a mockingbird", "Harper lee")

# library1 = Library()
# library1.add_books(book1)
# library1.add_books(book2)
# library1.display_books()
# library1.borrow_book(1)   # Already borrowed
# library1.borrow_book(99)  # Book not found
# library1.return_book(1)  # Should return successfully
# library1.return_book(1)  # Should say already available

# library1.search(title="THE GREAT GATSBY")  # Tests case-insensitivity
# library1.display_books()  # Checks final availability
# library1.borrow_book(1)
# library1.count_books()
library = Library()
checker= True
while checker:
    try: 

        print("Welcome! what do you went to do?")
        print("choice 1: add book")
        print("choice 2: borrow book")

        print("choice 3: return book")

        print("choice 4: search books")

        print("choice 5: count books")

        print("choice 6: display books")
        
        print("choice 7: exit")

        choice = int(input("Enter the choice: "))
   
        
        if(choice >=1 and choice<=7):
            if choice==1:
                book_id= int(input("Enter the book id: "))
                title = str(input("Enter the book title: "))
                author = str(input("Enter the book author: "))
                book = Book(book_id,title,author)
                library.add_books(book)
            elif choice==2:
                book_id= int(input("Enter the book id  you went to borrow: "))
                library.borrow_book(book_id)
            elif choice==3:
                book_id= int(input("Enter the book id you went to return: "))
                library.return_book(book_id)
            elif choice==4:
                tile_author= str(input("Enter the book title or anuthor to search the book: "))
                library.search(title=tile_author)
                
            elif choice==5:
                library.count_books()
            elif choice==6:
                library.display_books()
            
            elif choice ==7:
                
                    checker = False
                    print("Goodbye!")
        else:
            print("Please enter an integer with in the range of 1 to 6")
                
                
            
        
    except ValueError:
        
        print("Please enter intiger number only!")
    



