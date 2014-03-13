import webapp2, jinja2, os, urllib, io, re, logging
import markdown
from datetime import datetime
from google.appengine.ext import db
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'template')))

posts = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'articles')))

subject = "blog's name"


class MainPage(webapp2.RequestHandler):
    def get(self):
        list = []
        for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), 'articles/')):
            for name in files:
                if name.endswith('.md'):
                    title = ''
                    date = datetime.now()
                    tags = []
                    full_name = os.path.join(root, name)
                    f = open(full_name, 'r')
                    line = f.readline().strip()
                    while line != '':
                        mi = line.split(':', 1)
                        if len(mi) >= 2:
                            kind = mi[0].strip().lower()
                            if kind == 'title':
                                title = mi[1].strip()
                            elif kind == 'date':
                                date = datetime.strptime(mi[1].strip(), '%Y-%m-%d %H:%M')
                            elif kind == 'tags':
                                tags = mi[1].strip().split(', ')
                        line = f.readline().strip()
                    f.close()
                    list.append((date, name.rsplit('.', 1)[0], title, tags))
        list.sort(reverse=True)

        contents = ''
        template = jinja_environment.get_template('index.html')
        count = 0
        for date, filename, title, tags in list:
            if count % 2 == 0:
                section = jinja_environment.get_template('sectiona.html')
            else:
                section = jinja_environment.get_template('sectionb.html')
            count = count + 1
            html = '<h2 class="section-heading"><a href="' + urllib.quote(filename) + '">' + title.decode('utf-8') + '</a></h2>'
            html += '<p class="lead" style="text-align:right;">' + date.strftime('%b %d, %Y') + '</p>'
            content = section.render({'content': html})
            contents = contents + content

        self.response.out.write(
            template.render({
                'contents': contents,
                'subject': subject
            })
        )        


class PostPage(webapp2.RequestHandler):
    def get(self):
        encoded = self.request.path[1:]
        word = urllib.unquote(encoded)
        template = jinja_environment.get_template('index.html')
        md = markdown.Markdown()
        post = posts.get_template(word + '.md')
        buf = io.StringIO(post.render())
        line = buf.readline().strip()

        title = ''
        tags = []
        date = datetime.now()
        while line != '':
            mi = line.split(':', 1)
            if len(mi) >= 2:
                kind = mi[0].strip().lower()
                if kind == 'title':
                    title = mi[1].strip()
                elif kind == 'date':
                    date = datetime.strptime(mi[1].strip(), '%Y-%m-%d %H:%M')
                elif kind == 'tags':
                    tags = mi[1].strip().split(', ')
            line = buf.readline().strip()
        section = jinja_environment.get_template('sectionb.html')
        html = md.convert(buf.read())
        content = section.render({ 'content': html })

        disqus = jinja_environment.get_template('disqus.html')
        contentc = disqus.render ({
            'identifier': word,
            'subject': title
        })

        tagstr = ''
        for tag in tags:
            if tagstr == '':
                tagstr = tagstr + tag
            else:
                tagstr = tagstr + ', ' + tag
        self.response.out.write(
            template.render({
                'contents': content,
                'subject': title,
                'date': date.strftime('%b %d, %Y'),
                'disqus': contentc,
                'tags': tagstr
            })
        )

class FeedPage(webapp2.RequestHandler):
    def get(self):
        def removeframe(data):
            def escape(t):
                return (t
                    .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    .replace("'", "&#39;").replace('"', "&quot;")
                    )
            p = re.compile(r'<iframe.*</iframe>')
            return escape(p.sub('', data))


        list = []
        for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), 'articles/')):
            for name in files:
                if name.endswith('.md'):
                    title = ''
                    date = datetime.now()
                    tags = []
                    full_name = os.path.join(root, name)
                    f = open(full_name, 'r')
                    line = f.readline().strip()
                    while line != '':
                        mi = line.split(':', 1)
                        if len(mi) >= 2:
                            kind = mi[0].strip().lower()
                            if kind == 'title':
                                title = mi[1].strip()
                            elif kind == 'date':
                                date = datetime.strptime(mi[1].strip(), '%Y-%m-%d %H:%M')
                            elif kind == 'tags':
                                tags = mi[1].strip().split(', ')
                        line = f.readline().strip()
                    data = f.read()
                    f.close()
                    list.append((date, name.rsplit('.', 1)[0], title, tags, data))
        list.sort(reverse=True)

        md = markdown.Markdown()
        feeds = []
        count = 0
        for date, filename, title, tags, data in list:
            if count >= 10:
                break
            html = md.convert(data)
            feeds.append((title, urllib.quote(filename), removeframe(html), 
                date.strftime('%a, %d %b %Y %H:%M:%S +0900')))
            count = count + 1

        template = jinja_environment.get_template('feed.xml')
        self.response.headers['Content-Type'] = 'application/rss+xml'
        self.response.out.write(
            template.render({'items': feeds})
        )        




                
app = webapp2.WSGIApplication([
                    ('/', MainPage),
                    ('/feeds', FeedPage),
                    ('/.*', PostPage),
                ], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
 
