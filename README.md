# dataset-creation
 _Created in collaboration with [Suchit Jain](https://github.com/suchitj2702)_
 
The code scrapes images and captions from CommonCrawl web archives. Note that images are only downloaded if they are associated with a significant amount of text in English. The images are also filtered by:
1. Image resolution
2. Caption length
3. Image-caption matching
4. Number of recognizable English words
5. Presence of NSFW content

The library uses PyTorch, gzip, numpy, warcio, BeautifulSoup4, NLTK, NudeNet, OpenCV, Pandas, and wget.

## How-to
After installing the required libraries, run:
```python main.py```

To configure download and filtering parameters, modify parameters in `lib/config.py`
