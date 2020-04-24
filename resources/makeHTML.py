import pandas as pd

data = pd.read_excel("res.xlsx")

head = '''
<html>
<head>

<link href="style.css" media="all" rel="stylesheet"/>
</head>
'''

body = '''
<body>

<div class="container">
<img src="https://cdn.pixabay.com/photo/2015/09/02/13/08/way-918900_1280.jpg" style="width:100%;height:50%">
<div class="text-block">
    My <br> Data Science <br>Resources
  </div>	
</div>

<div class="header">
  Learning Data science is nothing less than taking an arduous and hard journey. 
  So much to learn and so many paths to choose that it leaves us confused at times.
  
  <h2>Books For Data Science</h2>
  <p> These books are some of the most important texts when it comes to Data Science. And something that should be in the bookshelves of every Data Scientist. 
    <br>You can't go wrong with any of these books.
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
    text += f'''<div class="tile" style="background-image: url('{img}');">
    <div class="textWrapper"><h3><a href="{url}">{h1}</a></h3>
      <div class="content">The western part of the Pont de Bir-Hakeim seen at night. Buildings of the 16th arrondissement of Paris are visible in the background.</div>
    </div></div>'''

body += '<div class="imageGrid">'+text+'</div>' 



# Courses
body += '''
<br>
<hr class="rounded">
<div class="header">
  <h2>Online Data Science Masters</h2>
  <p> Although you can find many resources for Data Science on the internet, sometimes having a degree helps as it provides one with structured learning.
  <br>I have not yet done a masters but these would be one of my choices if I were to do one.
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

  <p> Although you can find many resources for Data Science on the internet, sometimes having a degree helps as it provides one with structured learning.
  <br>I have not yet done a masters but these would be one of my choices if I were to do one.
  </p>
</div>
'''

mcembed = '''
<!-- Begin Mailchimp Signup Form -->
<div id="mailchimp">
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
