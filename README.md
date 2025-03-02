# Goal

ShELF is a web-based application designed to help librarians and library staff efficiently shelf-read books. It's primary goal is to minimize human error in this often tedious and labor-intensive task, which is essential for regular inventory control. This application is especially beneficial for individuals who may have health conditions that affect focus and recall, as well as for library staff who are new to the LOC Call number system. ShELF is intended to be integrated into a regular shelf-reading schedule, offering an in-house solution to address limited staff availability and resources.

Cobuilt with [@zeedmund](https://github.com/zeedmund)

![Screenshot of Shelf](https://github.com/hunordori/shelf/blob/main/screenshots/Result%20Page%202.jpg)

# How to install it?

## Manual Installation
You have to clone the repository to your machine. Follow these steps:

1. Open your terminal or command prompt.
2. Navigate to the directory where you want to clone the repository.
3. Run the command `git clone https://github.com/hunordori/shelf-organizer.git`.
4. Wait for the repository to be cloned.
5. Navigate to the cloned repository directory. `cd shelf-organizer`
6. Create a virtual environment. `python -m venv .venv`
7. Activate the virtual environment. `source .venv/bin/activate`
8. Install the required packages. `pip3 install -r requirements.txt`
9. Find the manage.py file and type in `python3 manage.py runserver` to start the development server.
10. Open your web browser and navigate to `http://127.0.0.1:8000/` to see the application in action.

## Automated Installation
You can also use the provided script to automate the installation process. Follow these steps:

1. Open your terminal or command prompt.
2. Navigate to the cloned repository directory. `cd shelf-organizer`
(If you are on a Mac you have to run `sudo chmod +x install.sh` to make the script executable)
3. Run the script `./install.sh` to install the application.

# How to use it?

If you want to test, use the provided database file with the following username and password:

- Username: admin
- Password: shelf_pass

After you opened the application in your browser.

1. Navigate to the "Books" page.
2. Open up a new browser window with the following URL: `http://127.0.0.1:8000/books/reorder/`
3. Copy some barcodes from the "Books" page to the "Barcodes" field.
4. Click "Submit" to reorder the books and see the result.

You can find a sample_library_data.csv file in the data directory.

## Use with your own data

To start, you need a .csv file with the following data and formatting:

title,barcode,call_number (as columns)

See the example in shelf_organizer/data/sample_library_data.csv

1. Rename or delete the current db.sqlite3 file.
2. Run the command `python manage.py migrate` to create the necessary tables. (Make sure the virtual environment is activated)
3. Run `python3 manage.py createsuperuser` to create a superuser account.
4. Run `python manage.py runserver` to start the development server.
5. Open your web browser and navigate to `http://127.0.0.1:8000/` to see the application in action.
6. Log in with the superuser account and import your .csv file by clicking on the "Import Books" button on.


# Known Issues and further development

- Currently the application only works with .csv data
- The result page is static, there is a plan to display some visual ques, like colored boxes or images.
- To further improve the user experience, we plan to add a feature that automatically rearranges the result table after the user checks off a step
