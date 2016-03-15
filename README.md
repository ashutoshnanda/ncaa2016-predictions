#Method

I'll try a few different methods:

1. Predict number of wins directly and compare teams on the basis of that (a la David Stein and Sports Statistics)
2. Predict point values for each game and play out the tournament

#Data

Getting Tournament Structure - [Example for 2001](http://www.sports-reference.com/cbb/postseason/2001-ncaa.html)  
Data Source URLs: 
```python 
url_format = "http://www.sports-reference.com/cbb/postseason/%d-ncaa.html"
years = range(2001, 2016 + 1)
urls = [url_format % year for year in years]
```