# Project 1 - Movie Trailer Website

#### Description

This is a project, which features my favorite hundred movies.


![alt tag](https://github.com/jocialmedia/fullstack_nanodegree_project1_movie-trailer-website/blob/master/moviepage_screenshot.png)

This is the full screen view of the page.

![alt tag](https://github.com/jocialmedia/fullstack_nanodegree_project1_movie-trailer-website/blob/master/moviepage_menu.png)

This is the menu, which allows sorting the movies by name, year, runtime and my own rating.

![alt tag](https://github.com/jocialmedia/fullstack_nanodegree_project1_movie-trailer-website/blob/master/moviepage_detailinfo.png)

After clicking on any of the movies an info box appears, which shows the movie poster and detailed information. This also includes separate buttons which link to the films Wikipedia article or its entry in the International Movie Database (IMDB). Other buttons open a direct search for the film title at Bing, DuckDuckGo or Google. In the lower right corner of the info box the movies trailer is embedded.


#### Installation 

Step 1. Make sure you have PHP, Git and Python 2.7. installed on your computer and your virtual server running.

Step 2. Get this code on your computer by going into the designated root folder of your virtual server (f.e. **htdocs**) and run

```
git clone https://github.com/jocialmedia/fullstack_nanodegree_project1_movie-trailer-website.git
```

Step 3. Open Python and run the file **moviepage_install.py**. 

![alt tag](https://github.com/jocialmedia/fullstack_nanodegree_project1_movie-trailer-website/blob/master/moviepage_installmessages.png)

This is what you should see.

Step 4. Open the browser of your choice and go to the project folder **fullstack_nanodegree_project1_movie-trailer-website**. After running the install-file in Python, you should now find a folder **moviepage** with an **index.html** which will be automatically found and read by your browser.


#### How does it work? 

* The file **moviepage_classes.py** contains the definition of the class Movie with its attributes.

* The file **moviepage_install.py** contains a hundred separate calls of the class **Movie**, with detail information like the name, the year, the runtime and the link to the English Wikipedia article. The list **movie_list** at the end of the file contains the names of all hundred separate calls which where mentioned before. Upon execution the file runs the function **create_movie_page** from the **filemoviepage_generator_script.py** and hands over the list **movie_list**.

* The function **create_movie_page** in **moviepage_generator_script.py** activates several functions. The first one **create_json_file_with_movie_info()** is executed for every single item of the list **movie_list**. It calls the function in the file **moviepage_install.py** and initiates the class **Movie** for each single movie and returns the values, which are saved together in a json-file called **moviepage_databasefile.json**. The other three functions **create_css_file_for_movie_page()**, **create_javascript_file_for_movie_page()** and **create_html_file_for_movie_page()** create the files **moviepage.css**, **moviepage.js** and **index.html** from the raw-code, which is already prepared and stored as string values. The function **copy_directory_with_movie_posters()** does exactly what its name implies and copies the prepared hundred image files into the new file structure.


# Additional Remarks

##### How did you pick the movies?
I used my own already existing list of movies, which I rated with 1 to 10 stars. I excluded franchise movies like "Lord Of the Rings", "Star Wars" or "Matrix" to get a more diverse and interesting selection.  Afterwards I compiled a list of the best ones with a rating from 8 and higher and came to a number of exactly a hundred.


##### Why do you create a json-file from a hundred single Python class calls? 
Because I found myself in kind of a dilemma. On the one hand I wanted to create a website with high usability, which lets the user manipulate the order of the movies and necessitates the use of Json and Javascript. On the other hand I did not want to leave the framework of this exercise, which focuses on "a page, which is dynamically generated from a Python data structure". So I found it to be an interesting solution to create the basic list in MySQL, export it to Json and use a separate Python file to recreate the hundred single class calls in moviepage_install.py.

##### Which additional resources did you use?
* [Udacity](https://www.udacity.com/course/nd004) (Code fragments)
* [Jquery](https://jquery.com/) (Code)
* [Twitter Bootstrap](http://getbootstrap.com) (Layout)
* [Wikipedia](http://www.wikipedia.org) (Information, Movie-Posters, Wikipedia-Url)
* [IMDB](http://www.imdb.com) (IMDB-Ids)
* [Youtube](https://www.youtube.com) (Youtube-Ids for Trailer)

--- 
This was done for **Project 1 - Movie Trailer Website**
as part of the [Full Stack Web Developer Nanodegree at Udacity.com](https://www.udacity.com/course/nd004)
March 2015
