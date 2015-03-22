# import dependencies
import webbrowser
import re
import json
import shutil
import os

# define content for html file
html_content = '''
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>My Favorite Movies</title>
        <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
        <link rel="stylesheet" href="moviepage.css">
        <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
        <script src="moviepage.js"></script>
       <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    </head>
    <body>

    <!-- Modal for Detailinfo -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">close</a>
          <div class="scale-media" id="inject_detailinfo">
          </div>
        </div>
      </div>
    </div>

    <!-- Modal for About -->
    <div class="modal" id="modal_about">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">close</a>
          <div class="scale-media" id="inject_aboutinfo">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
      <div class="navbar navbar-fixed-top" role="navigation">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">My Favorite Movies</a>
      </div>
      <ul class="nav navbar-nav navbar-right">
        <li class="dropdown">
          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">Order results <span class="caret"></span></a>
          <ul class="dropdown-menu" role="menu">
            <li onclick="showMyMovies('name_asc')" ><a href="#">Name (A-Z)</a></li>
            <li onclick="showMyMovies('name_desc')" ><a href="#">Name (Z-A)</a></li>
            <li class="divider"></li>
            <li onclick="showMyMovies('year_asc')" ><a href="#">Year (oldest-youngest)</a></li>
            <li onclick="showMyMovies('year_desc')" ><a href="#">Year (youngest-oldest)</a></li>
            <li class="divider"></li>
            <li onclick="showMyMovies('runtime_asc')"><a href="#">Runtime (shortest-longest)</a></li>
            <li onclick="showMyMovies('runtime_desc')"><a href="#">Runtime (longest-shortest)</a></li>
            <li class="divider"></li>
            <li onclick="showMyMovies('myrating_asc')"><a href="#">Rating (lowest-highest) </a></li>
            <li onclick="showMyMovies('myrating_desc')"><a href="#">Rating (highest-lowest)</a></li>
          </ul>
        </li>
        <li onclick="showAbout()" data-toggle='modal' data-target='#modal_about'><a href="#">About</a></li>
      </ul>

     </div><!-- .navbar -->
    
    <div class="content">
     <div id="injectmovies"></div> 
    </div>
  </body>
</html>
'''

# define content for css file
css_content = '''
body {
    width: 100%;
    padding-top: 48px;
    overflow: auto;
}

.navbar {
    background-color: #701112;
    color: #ffffff;
}

.navbar-brand, .navbar-brand:visited {
    background-color: #701112;
    color: #ffffff;
}

.navbar-brand:hover {
    color: #FA8995;
}

.content {
    width: 100%;
    padding: 0;
    margin: 0;
}

#moviebox {
    float: left;
    position: relative;
    margin-right: -1;
    margin-left: -1;
    padding: 0;
}

#moviebox img {
    background-color: white;
    opacity: .2; 
    filter: Alpha(Opacity=50);
}

#moviebox img:hover {
    opacity: 1; 
}

#moviename {
    position: absolute;
    margin-left: -100%;
    padding: 5px;
    margin-top: 95%;
    background-color: #701112;
    color: #ffffff;
    font-size: 16px;
    text-align: left;
    z-index: 10;
}

#orderby {
    position: absolute;
    margin-left: -100%;
    padding: 5px;
    margin-top: 80%;
    background-color: #701112;
    color: #ffffff;
    font-size: 16px;
    text-align: left;
    z-index: 10;
}

img {
    float: left;
    margin: 0;
    padding: 0;
    z-index: 5;
}

.filmmodal {
    padding: 5;
    height: 360px;
}

.filmmodal_poster {
    float: left;
    height: 100%;
    margin-right: 5px;
}

.filmmodal_poster img {
    height: 100%;
}

.filmmodal_info {
    float: left;
    height: 35%;
}

.filmmodal_trailer {
    float: left;
    height: 65%;
    width: 57%;
}

.aboutmodal {
    margin: 40px;
}

.button_imdb {
    background-color: #f3ce00;
    color: #fff;
}

.button_duckduckgo {
    background-color: #de5833;
    color: #fff;
}

.button_wikipedia {
    background-color: #D3D3D3;
    color: #fff;
}

.button_google {
    background-color: #4285f4;
    color: #fff;
}

.button_bing {
    background-color: #ffb900;
    color: #fff;
}

#trailer .modal-dialog {
    margin-top: 200px;
    width: 640px;
    height: 480px;
}

.hanging-close {
    position: absolute;
    top: 5px;
    right: 5px;
    z-index: 9001;
}

#trailer-video {
    width: 100%;
    height: 100%;
}

.movie-tile2 {
    margin-bottom: 20px;
    padding-top: 20px;
}

.movie-tile2:hover {
    background-color: #EEE;
    cursor: pointer;
}

.navbar-nav.navbar-right:last-child {
    margin-right: 0;
}

.navbar-nav>li>a {
    text-shadow: 0 0 0 0;
    color: #fff;
}

.navbar-nav>li>a:hover {
background-color: #fff;
color: #000;
}
'''

# define content for javascript file
javascript_content = '''
// add necessary zeros to ids to call filenames for movieposters, f.e. "099.jpg" instead of "99.jpg"
function getLeadingZeros(width, string, padding) { 
    return (width <= string.length) ? string : getLeadingZeros(width, padding + string, padding)
}

// open modal with info about movie
function showMyMovieInfo(id) {
$.getJSON('moviepage_databasefile.json', function(moviedata) {
$("#inject_detailinfo").empty().append($("<div class='filmmodal'><div class='filmmodal_poster'><img src='moviepage_posters/"+getLeadingZeros(3,moviedata[id-1].id.toString(),'0')+".jpg'></div><div class='filmmodal_info'><h4>"+moviedata[id-1].name+"</h4><b>Year:&nbsp;</b>"+moviedata[id-1].year+"&nbsp;&nbsp;<b>Runtime:&nbsp;</b>"+moviedata[id-1].runtime+"&nbsp;&nbsp;<b>My Rating:&nbsp;</b>"+moviedata[id-1].myrating+"<br/><br/>&nbsp;<a href='"+moviedata[id-1].url_wikipedia+"' target='_blank'><span class='btn btn-xs button_wikipedia'>Wikipedia</span></a>&nbsp;<a href='http://www.imdb.com/title/"+moviedata[id-1].id_imdb+"' target='_blank'><span class='btn btn-xs button_imdb'>IMDB</span></a>&nbsp;<a href='https://duckduckgo.com/?q="+moviedata[id-1].name+"' target='_blank'><span class='btn btn-xs button_duckduckgo'>duckduckgo</span></a>&nbsp;<a href='https://google.com/?q="+moviedata[id-1].name+"' target='_blank'><span class='btn btn-xs button_bing'>google</span></a>&nbsp;<a href='https://www.bing.com/search?q="+moviedata[id-1].name+"' target='_blank'><span class='btn btn-xs button_google'>bing</span></a></div><div class='filmmodal_trailer'><iframe src='http://www.youtube.com/embed/"+moviedata[id-1].id_trailer+"?rel=0' width='100%' height='100%' frameborder='0'></iframe></div></div>"));
});
}

// open modal with info about page
function showAbout() {
$("#inject_aboutinfo").empty().append($("<div class='aboutmodal'>This was done by <a href='http://joachim.dethlefs.eu/' target='new'>Joachim Dethlefs</a> for <b>Project 1 - Movie Trailer Website</b/><br/>as part of the <a href='https://www.udacity.com/course/nd004' target='_new'>Full Stack Web Developer Nanodegree at Udacity.com</a><br/>March 2015<br/><br/>All names of movies, products, brands and companies as well as the movie posters belong to the respective owners.<br/><br/>This code and more information about the installation and the background is available on Github at <a href='https://github.com/jocialmedia/fullstack_nanodegree_project1_movie-trailer-website' target='_new'>github.com/jocialmedia/fullstack_nanodegree_project1_movie-trailer-website</a></div>"));
}

// show single box with picture, name and information depending on choosen order
function showMoviebox(moviedata, orderby) {
var functionoutput = '';
    functionoutput += "<div onclick='showMyMovieInfo("+moviedata.id+")' id='moviebox' data-trailer-youtube-id='o4gHCmTQDVI' data-toggle='modal' data-target='#trailer'><div id='img'><span class='loadafter'></div><img src='moviepage_posters/"+getLeadingZeros(3,moviedata.id.toString(),'0')+".jpg'><span><span id='moviename'>"+moviedata.name+"</span><span id='orderby'>";
        if (orderby == 'name_asc' || orderby == 'name_desc') {
            functionoutput +=""+moviedata.id+".";
        } else if (orderby == 'year_asc' || orderby == 'year_desc') { 
            functionoutput +=""+moviedata.year+"";
        } else if (orderby == 'runtime_asc' || orderby == 'runtime_desc') {
            functionoutput +=""+moviedata.runtime + " min";
        } else if (orderby == 'myrating_asc' || orderby == 'myrating_desc') {
            functionoutput +=""+moviedata.myrating + "/10 Stars";
        };
    functionoutput += "</span></div>";
    return functionoutput;
}

// sort the movies by name, year, runtime or rating
function sortTheData(data, condition) {

if (condition == 'name_asc')
{
    data.sort(function(a, b)
    {
        if(a.name.toUpperCase() > b.name.toUpperCase()) {
            return 1;
        } else if (a.name.toUpperCase() < b.name.toUpperCase()) {
            return -1;
        } else if (a.year > b.year) {
            return 1;
        } else if (a.year < b.year) {
            return -1;
        } else {
            return 0;
        }
    })
} else if (condition == 'name_desc')
{
    data.sort(function(a, b)
    {
        if(a.name.toUpperCase() < b.name.toUpperCase()) {
            return 1;
        } else if (a.name.toUpperCase() > b.name.toUpperCase()) {
            return -1;
        } else if (a.year > b.year) {
            return 1;
        } else if (a.year < b.year) {
            return -1;
        } else {
            return 0;
        }
    })
} else if (condition == 'year_asc')
{
    data.sort(function(a, b)
    {
        if(a.year > b.year) {
            return 1;
        } else if (a.year < b.year) {
            return -1;
        } else if (a.name > b.name) {
            return 1;
        } else if (a.name < b.name) {
            return -1;
        } else {
            return 0;
        }
    })
} else if (condition == 'year_desc')
{
    data.sort(function(a, b)
    {
        if(a.year < b.year) {
            return 1;
        } else if (a.year > b.year) {
            return -1;
        } else if (a.name > b.name) {
            return 1;
        } else if (a.name < b.name) {
            return -1;
        } else {
            return 0;
        }
    })
} else if (condition == 'runtime_asc')
{
    data.sort(function(a, b)
    {
        if(Number(a.runtime) > Number(b.runtime)) {
            return 1;
        } else if (Number(a.runtime) < Number(b.runtime)) {
            return -1;
        } else if (a.name > b.name) {
            return 1;
        } else if (a.name < b.name) {
            return -1;
        } else {
            return 0;
        }
    })
} else if (condition == 'runtime_desc')
{
    data.sort(function(a, b)
    {
        if(Number(a.runtime) < Number(b.runtime)) {
            return 1;
        } else if (Number(a.runtime) > Number(b.runtime)) {
            return -1;
        } else if (a.name > b.name) {
            return 1;
        } else if (a.name < b.name) {
            return -1;
        } else {
            return 0;
        }
    })
} else if (condition == 'myrating_asc')
{
    data.sort(function(a, b)
    {
        if(Number(a.myrating) > Number(b.myrating)) {
            return 1;
        } else if (Number(a.myrating) < Number(b.myrating)) {
            return -1;
        } else if (a.name > b.name) {
            return 1;
        } else if (a.name < b.name) {
            return -1;
        } else {
            return 0;
        }
    })
} else if (condition == 'myrating_desc')
{

    data.sort(function(a, b)
    {
        if(Number(a.myrating) < Number(b.myrating)) {
            return 1;

        } else if (Number(a.myrating) > Number(b.myrating)) {
            return -1;
        } else if (a.name > b.name) {
            return 1;
        } else if (a.name < b.name) {
            return -1;
        } else {
            return 0;
        }
    })
}
}


// show movies
function showMyMovies(orderby) {

    // set order by name_asc as standard fallback option
    if (!orderby) {
        var orderby = 'name_asc';
    };
    
// load the info from the json file
$.getJSON('moviepage_databasefile.json', function(moviedata) {

    // initiate variable output
    var output = '';

    // sort the moviedata
    sortTheData(moviedata, orderby);

    // create the moviebox for every movie
    for (i = 0; i < moviedata.length; ++i) {
          output += showMoviebox(moviedata[i],orderby);
    };      

    // inject the output into the page
    $('#injectmovies').html(output);

    // get the width and height of the screen
    var documentwidth = $(document).width();
    var documentheigth = $(document).height();

    // inject the appropiate values for width and height in the moviebox
    $("#moviebox").width(((documentwidth/6)-3));
    $("#moviebox").height((documentwidth/6)*1.5);
    $("img").width(((documentwidth/6)-3));
    $("img").height((documentwidth/6)*1.5);
});
};





$(document).ready(function() {
    // when page loads for the first time call function sorted by name
    showMyMovies('name_asc');
    // when the browserwindow is resized, the movies are called again to get the layout responsive
    window.onresize = function() {
        showMyMovies('name_asc');
    };
});



$(document).on('click', '.hanging-close, .modal', function (event) {
    // Remove the src so the player itself gets removed, as this is the only
    // reliable way to ensure the video stops playing in IE
    $(".filmmodal_trailer").empty();
});

'''

  
# function to create a json file with the movie information
def create_json_file_with_movie_info(movies):

    # initialize variable for artifical id
    i = 0;
    
    # initialize variable for moviedata
    moviedata = []

    # loop through the array with moviedata one movie at a time
    for movie in movies:
        
        # count up artifical id
        i = i + 1
        
        # collect the movieinformation in the variable moviedata
        moviedata.append({'id': i, 'name' : movie.title, 'year' : movie.year, 'runtime' : movie.runtime, 'myrating' : movie.myrating, 'id_imdb' : movie.id_imdb, 'id_trailer' : movie.id_trailer, 'url_wikipedia' : movie.url_wikipedia})

    # create a file called 'movies_databasefile'
    with open("moviepage/moviepage_databasefile.json", "w") as outfile:

        # sage the content of variable 'moviedata' in json format
        json.dump(moviedata, outfile)
        print "2. JSON file is ready."

# function to create a css-file
def create_css_file_for_movie_page():
  output = open('moviepage/moviepage.css', 'w')
  output.write(css_content)
  output.close()
  print "4. CSS file is ready."

# function to create a javascript-file
def create_javascript_file_for_movie_page():
  output = open('moviepage/moviepage.js', 'w')
  output.write(javascript_content)
  output.close()
  print "5. Javascript file is ready."

# function to create a javascript-file
def copy_directory_with_movie_posters():
  if not os.path.exists('moviepage/moviepage_posters'):
    os.makedirs('moviepage/moviepage_posters')
  file_list = os.listdir("moviepage_posters")
  for file_name in file_list:
    shutil.copy('moviepage_posters/' + file_name, 'moviepage/moviepage_posters/' + file_name)
  print "3. Movieposters are ready."
  

# function to create a html-file
def create_html_file_for_movie_page():
  output_file = open('moviepage/index.html', 'w')
  output_file.write(html_content)
  output_file.close()
  print "6. Html file is ready."


# create the json-file with the movie-information
def create_movie_page(movies):
  print "Installation process started."
  if not os.path.exists('moviepage'):
    os.makedirs('moviepage')
  print "1. Folder moviepage is ready."
  create_json_file_with_movie_info(movies)
  copy_directory_with_movie_posters()    
  create_css_file_for_movie_page()
  create_javascript_file_for_movie_page()
  create_html_file_for_movie_page()
  print "Installation process finished."
  print "Open the moviepage/index.html in your browser now."
