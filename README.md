

# ivy
Command line utility facilitating the Ivy Lee time management method

<h2>On The Ivy Lee Method</h2>
<img src="./ivy_lee.png">
<p><a href="https://en.wikipedia.org/wiki/Ivy_Lee">Ivy Ledbetter Lee</a> was a publicity expert and consultant in the late 1800s and early 1900s. He is credited with the development of what's become know as the Ivy Lee time management method.</p>

<p>The Ivy Lee method can be summarized as follows:</p>
<ul>
  <li>Before leaving work each day, write the 6 most important things you must do tomorrow.</li>
  <li>Evaluate and sort them based on their absolute priority.</li>
  <li>Arriving at work each day, begin the first item on the list and do not move on to the second until the first is completed.</li>
  <li>As the workday expires, move any unfinished items to a new list and repeat this procedure.</li>
</ul>
<p>The power of the method is that it requires the user to prioritize tasks, properly focus on one task at a time, and is so simple that it isn't a distraction in itself.</p>

<h2>About this software</h2>
<h3>Usage</h3>
<ul>
  <li>ivy project info: <code>ivy about</code>
  <li>marking items done: <code>ivy check &lt;num&gt;</code>, where &lt;num&gt; is an item's position in the list</li>
  <li>deleting an item: <code>ivy erase &lt;num&gt;</code>, where &lt;num&gt; is an item's position in the list</li>
  <li>this dialog: <code>ivy help</code></li>
  <li>viewing the list: <code>ivy list</code></li>
  <li>deleting all items: <code>ivy new</code></li>
  <li>rewriting items: <code>ivy rewrite &lt;num&gt; "new item description"</code>, where &lt;num&gt; is an item's position in the list.</li>
  <li>reordering items: <code>ivy put &lt;num&gt; &lt;num2&gt;</code>, where &lt;num&gt; is the position of the item to be moved and <num2> is the position to move it to</li>
  <li>marking items todo: <code>ivy uncheck &lt;num&gt;</code>, where &lt;num&gt; is an item's position in the list</li>
  <li>adding new items: <code>ivy write "text description of work item"</code>, with quoted text</li>
</ul>
