Geopull is a tool to crawl tumblr accounts for images, and extract GPS information(if available) from those images. It then does a coordinate lookup using Nominatim. Images are stored in the created images/username/ directory, so you can go back in and see which coordinates correspond to which pictures if you're interested to see.  

This uses the Tumblr API to do the heavy lifting, so you'll need to go get your API key and generate an OAUTH token, and enter them in the relevant variables in tumblecrawl.py    
Usage: ./geopull.py username  
Example: ./geopull.py abcnews  

If you don't like my code, too bad. Don't use it. 
