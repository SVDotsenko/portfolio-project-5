copy card number to clipboard before entering the donation page, and show tooltip
add tooltips

# Kind Heart Charity

Kind Heart Charity is a web-based application designed to facilitate and manage the process of charitable donations. The application is built using Django and JavaScript, with package management handled by pip for Python.  The application allows users to browse through various causes and make donations. Each donation is associated with its respective cause. Users can also track their donation history, providing a dynamic and interactive charity experience.  The application has two main user roles: User and Administrator. A User can browse the causes, make donations, and track their donation history. An Administrator, on the other hand, has the ability to add, delete, and modify causes in the application, providing comprehensive management of the charity's causes.  The application ensures secure user authentication and role-based access to various features. It also includes robust error handling and user notifications for a smooth user experience.  The project uses a PostgreSQL database for data storage, managed through Django's ORM.  The application's user interface is designed to be intuitive and user-friendly, ensuring a seamless user experience.

---

[View live project here](https://pp4-library-f562eb8422f8.herokuapp.com)

![Responsive design](static/img/readme/smartphones.png)

![Responsive design](static/img/readme/desktop.png)

## The application implements the following features:

- Access to the application is only possible through a login and password.
- The application has 2 user roles: Reader and Administrator.
- Registration of a new user (with the role of Reader) through the user interface.

Common functionality for both roles includes:

- Logging into the application through a login form.
- Viewing all books in the library.
- Editing information in the profile about the current user logged into the system, including changing the photo.
- If the user will try to access the route that is not exist, the user will be redirected to the 404 page.
- There are [tooltips](https://getbootstrap.com/docs/5.3/components/tooltips) for all interactive elements in the application which provide additional information about the
  action that will be performed after clicking on the element.
- There are [toasts](https://getbootstrap.com/docs/5.3/components/toasts) for all create, update and delete operations which provide current user details about
  what he\she has just done.
- All input fields in this application are mandatory and have a validation on the client side.

Reader functionality:

- Borrowing books from the library.
- Returning books to the library.
- Seeing books that are unavailable and who is reading them.
- Does not have access to the authors' page, if the user tries to access this page, the user will be redirected to the 403 page.
- On the profile page, view the books that the reader is currently reading.
- There was also implemented a special error handling for 500 error, which is simulated on the server side. To see
  it, you need to check checkbox on profile page.

Administrator functionality:

- Adding new book authors.
- Editing book authors.
- For Adding and Editing book authors operations, implemented complex validations on client and server sides.
  - Client side: the input field cannot be empty and should be at least 1 character long.
  - Server side: each word must start with a capital letter separated by a space.
- Deleting book authors.
- Adding new books.
- Editing existing books.
- Deleting existing books.
- If a book is already being read by someone, such a book cannot be edited and the author of such a book also cannot be edited. The book must be returned by the reader before it can be edited or deleted.

### Existing Features

- **Books**

  - Administrator:

    - View all books in the library.
      ![books admin](static/img/readme/books-admin.png)
    - Add a new book to the library.
    - Edit an existing book in the library.
    - Delete a book from the library.

      ![delete book](static/img/readme/delete-book.png)

    - The book must be return before deleting or editing.

      ![reading book](static/img/readme/delete-book-tooltip.png)

  - User:

    - View all books in the library.

      ![books user](static/img/readme/books-user.png)

    - Borrow a book from the library.

      ![get book](static/img/readme/get-book.png)

    - Return a book to the library.

      ![return book](static/img/readme/return-book.png)

    - See if someone is reading the book.

      ![reading book](static/img/readme/reading-book.png)

- **Authors**

  - Administrator:
    ![authors admin](static/img/readme/authors-admin.png)

    - Add a new author to the library.
    - Edit an existing author in the library.
    - Delete an author from the library.

      ![delete book](static/img/readme/delete-author.png)

    - See if the book is taken by any reader.

  - User:

    - Do not have access to see this page.
    - If a user tries to access this page, they will be redirected to the 403 page.

      ![403 page](static/img/readme/403.png)

- **My Profile**
  - Administrator:
    ![admin profile](static/img/readme/profile-admin.png)
    - Edit information about itself:
      - First name.
      - Last name.
      - Email.
      - Profile image
  - User:
    ![admin profile](static/img/readme/profile-user.png)
    - See the books that are currently reading.
    - Edit information about itself:
      - First name.
      - Last name.
      - Email.
      - Profile image.
    - Simulate error on server to see how work error handling for 500 error.

### Features Left to Implement

- Protection of routes by roles through decorators.
- Make a check so that you cannot enter the same title of a book by the same author twice.
- Pagination, if there is a lot of content.
- Use ajax to avoid page reloading.
- Returning a book from the profile page.

## GitHub Project Board

The project was managed using a [GitHub Project Board](https://github.com/users/SVDotsenko/projects/4)

## Data model

1. **User Model**: This is a built-in Django model that represents the users of your application. It includes fields for username, password, email, first name, and last name. The User model is used for authentication and authorization in the Django framework.

2. **ProfileImage Model**: This model is related to the User model with a one-to-one relationship. It represents the profile image of a user. It includes the following fields:

   - `user`: A one-to-one field linking to the User model. When a User instance is deleted, the associated ProfileImage instance will also be deleted.
   - `image`: A field that stores the image of the user's profile. It uses the Cloudinary service for image hosting.

3. **Author Model**: This model represents the authors of the books in your application. It includes the following field:

   - `name`: A character field with a maximum length of 200 characters that stores the name of the author.

4. **Book Model**: This model represents the books in your application. It includes the following fields:
   - `title`: A character field with a maximum length of 200 characters that stores the title of the book.
   - `author`: A foreign key field linking to the Author model. When an Author instance is deleted, the associated Book instances will not be deleted but the `author` field will be set to NULL.
   - `reader`: A foreign key field linking to the User model. It represents the user who is currently reading the book. When a User instance is deleted, the `reader` field in the associated Book instances will be set to NULL.

The User model handles user authentication, the ProfileImage model handles user profile images, the Author model represents book authors, and the Book model represents the books in application and their current reader.

## Technologies Used

### Languages Used

- [HTML5](https://en.wikipedia.org/wiki/HTML5)
- [CSS3](https://en.wikipedia.org/wiki/Cascading_Style_Sheets)
- [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
- [Python 3.9.19](https://www.python.org/)

### Frameworks, Libraries & Programs Used

1. [Google Fonts:](https://fonts.google.com)
   - Google fonts were used to import the 'Open Sans' font into the style.css file which is used on all pages throughout the project.
1. [Font Awesome 6.5.2:](https://fontawesome.com)
   - Font Awesome was used on all pages throughout the website to add icons for aesthetic and UX purposes.
1. [Bootstrap 5.3.3:](https://getbootstrap.com/docs/5.3/getting-started/introduction)
   - Bootstrap was used to assist with the responsiveness and styling of the website.
1. [jQuery 3.7.1:](https://jquery.com)
   - jQuery came with Bootstrap to make the navbar responsive but was also used to show tooltips.
1. [Google Chrome 124.0.6367.62:](https://www.google.com/chrome)
   - Google Chrome was used as a browser to render and debug this project.
1. [Django 4.2.11:](https://www.djangoproject.com)
   - Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.
   - There were also used other [libraries](requirements.txt) in this project.
1. [ElephantSQL:](https://www.elephantsql.com)
   - ElephantSQL was used to store data.
1. [Cloudinary:](https://cloudinary.com)
   - Cloudinary was used to store images.
1. [Node.js 20.12.2:](https://nodejs.org)
   - Node.js was used to run JavaScript unit-tests.
1. [npm 10.7.0:](https://www.npmjs.com)
   - npm was used as a package manager for installing [dependencies](package.json).
1. [JSHint:](https://jshint.com)
   - JSHint was [used](.jshintrc) to check the quality of JavaScript code.
1. [Jest 26.6.3:](https://jestjs.io)
   - Jest was [used](package.json) for writing unit-test for JavaScript part of this Project.
1. [Coverage 7.4.4:](https://coverage.readthedocs.io)
   - Coverage was used to measure code coverage of Python code.
1. [Git 2.39.1:](https://git-scm.com)
   - Git was used for version control to commit and Push code to GitHub.
1. [GitHub:](https://github.com)
   - GitHub was used to store the projects code after being pushed from Git.
1. [Heroku:](https://www.heroku.com)
   - Heroku was used to deploy the project.
1. [Bash 5.2.12:](https://www.gnu.org/software/bash/manual)
   - Bash was [used](coverage.sh) to automate running Test Coverage reports.
1. [GitHack:](https://raw.githack.com)
   - GitHack was used to render Code coverage reports when you click on it on this page.
1. [Far Manager 3.0.5700.0:](https://www.farmanager.com)
   - Far Manager was used to work with files.
1. [PyCharm 2024.1:](https://www.jetbrains.com/pycharm)
   - PyCharm was used to write all code for this project.
1. [Microsoft Windows 10.0.19045 Enterprise:](https://www.microsoft.com)
   - Windows was used as an operating system for development this project.

## Manual Testing

### Testing Login Functionality

1. **Testing login with correct credentials**

   - Navigate to the login page.
   - Enter the correct username and password.
   - Click the "Sign in" button.
   - Verify that you are redirected to the book page of the application.

2. **Testing login with incorrect credentials**
   - Navigate to the login page.
   - Enter incorrect username and password.
   - Click the "Sign in" button.
   - Verify that an error message is displayed.

### Testing Registration Functionality

1. **Testing registration with correct data**

   - Navigate to the registration page.
   - Enter correct data into all form fields.
   - Click the "Sign Up" button.
   - Verify that you are redirected to the book page with a successful login message.

2. **Testing registration with incorrect data**
   - Navigate to the registration page.
   - Enter incorrect data into one or more form fields.
   - Click the "Sign Up" button.
   - Verify that an error message is displayed.

### Testing Book Viewing Functionality

1. **Testing viewing the list of books**

   - Navigate to the books page.
   - Verify that a list of all books is displayed.

2. **Testing viewing book details**
   - Login as an Administrator.
   - Navigate to the books page.
   - Click on edit button one of the books.
   - Verify that a page with details of the selected book is displayed.

All additional features and functionality not explicitly mentioned in this section have also been thoroughly tested and are confirmed to be working correctly.

## Automation Testing

The entire project is covered by unit tests. Test coverage reports can be viewed in the following links:

- [Django Test Coverage Report](https://raw.githack.com/SVDotsenko/portfolio-project-4/master/htmlcov/index.html)
- [JavaScript Test Coverage Report](https://raw.githack.com/SVDotsenko/portfolio-project-4/master/coverage/lcov-report/index.html)

## Validator Testing

- HTML
  - All errors found by official W3C validator were fixed in separate [commit](https://github.com/SVDotsenko/portfolio-project-4/commit/b4cffffd38b8bc78106bc701044a4a9a3f8800b1).
- CSS
  - No errors were found when passing through the official (Jigsaw) validator
- JavaScript
  - No errors were found when passing through the JSHint validator according to [settings](.jshintrc).
- Python - All errors found by [CI Python Linter](https://pep8ci.herokuapp.com) were fixed in separate [commit](https://github.com/SVDotsenko/portfolio-project-4/commit/0379719df6edc0210029873d157f4d71d41e60da).
- Accessibility
  - I confirm that the colors and fonts chosen are easy to read and accessible by running it through lighthouse in devtools.
    ![lighthouse](static/img/readme/lighthouse.png)

## Unfixed Bugs

- Due to the fact that as an initial template I took an open source template and modified it, there may be unused
  classes in HTML and CSS, because I did not find tool that can check it automatically, I tried to find and remove it manually.

## Deployment

_By default, all console commands should be run in git bash terminal._

### Deployment To Heroku

The project was deployed to [Heroku](https://www.heroku.com).

The process of deploying this project to Heroku is consist of these main steps.

1. You should have accounts on GitHub, Heroku, Cloudinary, ElephantSQL.
2. You should create database on ElephantSQL and create models.
3. Deploy the project to Heroku.

#### Cloudinary

To get the CLOUDINARY_URL, you need to create an account on [Cloudinary](https://cloudinary.com) and follow the
instructions to get the URL:

1. Log in to your Cloudinary account.
2. Go to the "Dashboard" in section "Product Environment Credentials" you will see "API environment variable". It is your CLOUDINARY_URL.

#### ElephantSQL

To get the DATABASE_URL and SECRET_KEY, you need to create an account on [ElephantSQL](https://www.elephantsql.com) and
follow the instructions to get the URL:

1. Log in to your ElephantSQL account.
2. Click on "Create New Instance".
3. Name your database and select the "Tiny Turtle Free" plan.
4. Select the data center near you and click "Review".
5. Click "Create Instance".
6. Click on your new database instance you just created in section Details you will see Password and URL, this corresponds to the SECRET_KEY and DATABASE_URL.

#### Creating models on ElephantSQL

To create models on ElephantSQL you need to do the following steps:

1. Clone the project to your local machine, to do it run this command in your terminal:
   ```bash
   git clone https://github.com/SVDotsenko/portfolio-project-4.git
   ```
2. Follow the instruction in [env.md](env.md) file.
3. On your local machine, must be installed Python 3.9.19 or higher.
4. Create a virtual environment by running this command in your terminal:
   ```bash
   python -m venv venv
   ```
5. Activate the virtual environment by running this command in your terminal:
   ```bash
    source venv/Scripts/activate figure out how to do it on your OS!!!
    ```
4. Install all dependencies from the requirements.txt file by running this command in your terminal:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the following command in your terminal to create models on ElephantSQL:
   ```bash
   python manage.py migrate
   ```
6. Create a superuser by running this command in your terminal:
   ```bash
    python manage.py createsuperuser
    ```
7. The users with role Reader can be created through the sign-up form.

#### Heroku

1. [Fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)
   this project into you GitHub account:
1. Log in to your Heroku account.
1. Click on the "New" button and select "Create new app".
1. Choose a unique name for your app, select the region and click "Create app".
1. Go to the "Settings" tab and click on "Reveal Config Vars".
1. Add the following config vars from your [env.py](env.md) file

   - `DATABASE_URL`: Your ElephantSQL database URL.
   - `SECRET_KEY`: Your ElephantSQL secret key.
   - `CLOUDINARY_URL`: Your Cloudinary URL.
   - `DJANGO_DEBUG`: False.

1. In the "Deploy" tab, select "GitHub" as the deployment method.
1. Search for the repository you forked earlier and click "Search".
1. Click "Connect" to connect the repository to Heroku.
1. Scroll down to the "Manual deploy" section and click "Deploy Branch".
1. Once the deployment is complete, click "View" to open the live app.

## How to run this project locally

To run this project locally, you need to do the following steps:

1. Follow the instruction from section Creating models on ElephantSQL in this file.
2. Run this command:

   ```bash
   python manage.py runserver
   ```

### How to run unit tests locally and see coverage reports

To run unit tests locally and see coverage reports, you need:

1. On your machine must be installed Node.js.
2. Install dependencies from the package.json file by running this command:
   ```bash
   npm install
   ```
3. Run this command to run unit tests:
   ```bash
   ./coverage.sh
   ```
4. The browser should be opened a new tabs with the coverage reports.

## Credits

This [template](https://themewagon.com/themes/free-responsive-bootstrap-5-html5-charity-template-kindheart/) was adopted for the project.
https://templatemo.com/tm-581-kind-heart-charity
https://www.mrci.ie/donate/
https://youtu.be/oZwyA9lUwRk?si=PUu6H6EJB4H8dK6B