import pandas as pd

data = pd.read_excel("res.xlsx")

head = '''
<html>
<head>

<link href="style.css" media="all" rel="stylesheet"/>
<!-- BEGIN SHAREAHOLIC CODE -->
  <link rel='preload' href='//apps.shareaholic.com/assets/pub/shareaholic.js' as='script' />
  <script type="text/javascript" data-cfasync="false" async src="//apps.shareaholic.com/assets/pub/shareaholic.js" data-shr-siteid="fd1ffa7fd7152e4e20568fbe49a489d0"></script>
  
  <!-- END SHAREAHOLIC CODE -->

</head>
'''

body = '''
<body>
<section>
<div class="container">
<img src="https://cdn.pixabay.com/photo/2015/09/02/13/08/way-918900_1280.jpg" style="width:100%;height:50%">
<div class="text-block">
    Great <br> Data Science <br>Resources
  </div>  
</div>

<div class="header">
  Learning Data science is a journey in itself. And a mighty hard one at that. So much to learn and so many paths to choose that it leaves us confused at times. 
  I get many questions regarding how I learned Data Science? Or which books I find good? So I thought of adding the resources I found useful to this page. 
  As you may understand, this is an ever increasing list so it might help to bookmark this page.
  
  <h2>Books For Data Science</h2>
  <p> These books are some of the most important texts when it comes to Data Science. And something that should be in the bookshelves of every Data Scientist. 
    <br>You just can't go wrong with any of these books.
  </p>
</div>
'''

# Handling Books

books = data[data['h1']=='Books'][['img','url']].sample(frac=1)
buckets = ['','','','']
for i, row in books.iterrows():
    img = row['img']
    url = row['url']
    buckets[i%4] += f'<a href="{url}"><img src="{img}" style="width:100%"></a>'

buckets = " ".join(['<div class="column">'+x+'</div>' for x in buckets])

body += '<div class="row"> ' + buckets + '</div>'

# Degrees
body += '''
<br>

<hr class="rounded">
<div class="header">
  <h2>Online Data Science Masters</h2>
  <p> Although you can find many resources for Data Science on the internet, sometimes having a degree helps as it provides one with structured learning. 
  And a lot of people are looking to do a degree with their ongoing jobs. 
  <br>I have not yet done a masters but these would be one of my choices if I were to do one.
  </p>
</div>
'''

degrees = data[data['h1']=='Online Degrees'].sample(frac=1)
text = ''
for i, row in degrees.iterrows():
    img = row['img']
    url = row['url']
    h1 = row['name']
    h2 = row['h2']
    text += f'''<div class="tile" style="background-image: url('{img}');">
    <div class="textWrapper"><h3><a href="{url}">{h1}</a></h3>
      <div class="content">{h2}</div>
    </div></div>'''

body += '<div class="imageGrid">'+text+'</div>' 



# Courses
body += '''
<br>
<hr class="rounded">
<div class="header">
  <h2>Online Courses</h2>
  <p>  In his book, The Paradox of Choice — Why More Is Less, Schwartz argues that eliminating consumer choices can greatly reduce anxiety for shoppers. 
  And the same remains true for Data Science courses as well. So here are the courses that I found are the best when it comes to Data Science. 
  Do take a look at this <a href="https://towardsdatascience.com/top-10-resources-to-become-a-data-scientist-in-2020-99a315194701" style="color:red">post</a> also for more information about these courses.
  </p>
</div>
'''

courses = data[data['h1']=='Courses'].sample(frac=1)
dist_h2 = courses.h2.unique()
text = ''
for h2 in dist_h2:
  subset = courses[courses['h2']==h2]
  text+=f'''
  <h3>{h2}</h3><ul>
  '''
  for i, row in subset.iterrows():
      url = row['url']
      name = row['name']
      text += f'''
      <li><a href="{url}" style="color:black">{name}</a></li>
      '''
  text+='</ul>'

body += text

body += '''
<br>
<div class="header">

  As you all know I write beginner friendly Data Science posts. 
  Follow me up at <a href="https://medium.com/@rahul_agarwal" style="color:red">Medium</a> or Subscribe to my blog below to be informed about them. 
  As always, I welcome feedback and constructive criticism and can be reached on Twitter @mlwhiz. 
  Also do share this page on your social as sharing is caring.
  </p>
</div>


'''

mcembed = '''
<!-- Begin Mailchimp Signup Form -->
<div id="mailchimp">
<div class="shareaholic-canvas" data-app="share_buttons" data-app-id="28372088"></div><br>
<form action="https://mlwhiz.us15.list-manage.com/subscribe/post?u=4e9962f4ce4a94818bcc2f249&amp;id=87a48fafdd" method="post" id="mc-embedded-subscribe-form" name="mc-embedded-subscribe-form" class="validate" target="_blank" novalidate>
    <div id="mc_embed_signup_scroll">
<div class="mc-field-group">
  <input type="email" value="Enter Your Mail" name="EMAIL" class="required email" id="mce-EMAIL" onfocus="if(this.value==this.defaultValue)this.value='';" onblur="if(this.value=='')this.value=this.defaultValue;">
</div>
  <div id="mce-responses" class="clear">
    <div class="response" id="mce-error-response" style="display:none"></div>
    <div class="response" id="mce-success-response" style="display:none"></div>
  </div>    <!-- real people should not fill this in and expect good things - do not remove this or risk form bot signups-->
    <div style="position: absolute; left: -5000px;" aria-hidden="true"><input type="text" name="b_4e9962f4ce4a94818bcc2f249_87a48fafdd" tabindex="-1" value=""></div>
    <div class="clear"><input type="submit" value="Subscribe" name="subscribe" id="mc-embedded-subscribe" class="button"></div>
    </div>
</form>

</div>

<!--End mc_embed_signup-->
'''

fullhtml = head + body + mcembed+'''</body></html>'''
print(fullhtml)
