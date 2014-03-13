# GaeMdBlog

GaeMdBlog is a blog using Markdown on the Google App Engine. 

GaeMdBlog = [Google App Engine](https://developers.google.com/appengine) + [Markdown](http://daringfireball.net/projects/markdown/) + [Bootstrap](http://getbootstrap.com)

## Customize your blog

 - app.yaml

```
allication: {{your_app_id}}
```

 -  main.py

```
subject = "{{your_blog_name}}"
```

 -  template/disqus.html

```
var disqus_shortname = '{{your_disqus_shortname}}'
```

 -  index.html
	
	customize your templeates (title, links, etc)
	
## Write your post

1. Your markdown text to /articles

```
title: Lorem ipsum
date: 2014-03-10 12:17
tags: Lorem ipsum

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut vitae gravida est, vitae ultricies elit. Pellentesque et dolor venenatis, sollicitudin orci a, dapibus odio. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Morbi neque orci, ultrices in mauris quis, placerat cursus enim. Vestibulum ut mi orci. Etiam rutrum dignissim feugiat. Praesent scelerisque tortor nec scelerisque consequat. Mauris nec tortor faucibus, gravida lacus id, vehicula libero.
```

2. upload your applicaiton

```
appcfg.py update gaemdblog/
```

## License

Code released under the MIT License.

it includes :

 - [Bootstrap](http://getbootstrap.com/)
 - bootstrap template : [Start Bootstrap > Landing Page](http://startbootstrap.com/landing-page)
 - [Python-Markdown](https://pypi.python.org/pypi/Markdown)


