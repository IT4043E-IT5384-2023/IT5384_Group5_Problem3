# IT5384_Group5_Problem3
<!--TABLE of contents //-->
<br>
<hr>
<h2 id="Prerequisites">Prerequisites </h2>
<li> Internet Connection </li>
<li> Python 3.6+ </li>
<li> Chrome or Firefox browser installed on your machine </li>
<hr>


First, you need to run install the requirements: 
```python
pip install -r requirement.txt
```
RUN
```
python crawler.py
```

<br>
<div id="profileDetailArgument">
<p><code>get_profile_details()</code> arguments:</p>

<table>
    <thead>
        <tr>
            <td>Argument</td>
            <td>Argument Type</td>
            <td>Description</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>twitter_username</td>
            <td>String</td>
            <td>Twitter Username</td>
        </tr>
        <tr>
            <td>output_filename</td>
            <td>String</td>
            <td>What should be the filename where output is stored?.</td>
        </tr>
        <tr>
            <td>output_dir</td>
            <td>String</td>
            <td>What directory output file should be saved?</td>
        </tr>
        <tr>
            <td>proxy</td>
            <td>String</td>
            <td>Optional parameter, if user wants to use proxy for scraping. If the proxy is authenticated proxy then the proxy format is username:password@host:port.</td>
        </tr>
    </tbody>
</table>
<hr>
<br>
<div id="profileOutput">
<p>output</p>

<table>
    <thead>
        <tr>
            <td>Key</td>
            <td>Type</td>
            <td>Description</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Topic</td>
            <td>String</td>
            <td>topic of the tweet</td>
        </tr>
        <tr>
            <td>Tweet</td>
            <td>String</td>
            <td>tweet</td>
        </tr>
        <tr>
            <td>Username</td>
            <td>Integer</td>
            <td>Username of tweet</td>
        </tr>
        <tr>
            <td>Reposts</td>
            <td>Integer</td>
            <td>Number of Reposts of tweet</td>
        </tr>
        <tr>
            <td>likes</td>
            <td>Integer</td>
            <td>Number of likes of tweet</td>
        </tr>
        <tr>
            <td>Views</td>
            <td>Integer</td>
            <td>number of views</td>
        </tr>
        <tr>
            <td>Replies</td>
            <td>String</td>
            <td>Replies of Reposts of tweet</td>
        </tr>
        <tr>
            <td>Date</td>
            <td>String</td>
            <td>Date of the tweet</td>
        </tr>
    </tbody>
</table>
</div>
<br>
<hr>

Output:
```javascript
{
{"Topic":"cosmos","Username":"Nature & Cosmos\n@nature2cosmos\n\u00b7\n17h","Tweet":"The Sun is 20 years old.\nYes, 20 \"galactic\" years.\n\n Understanding Meaning.","Likes":56,"Views":"5.1K","Reposts":12.0,"Replies":null,"Date":"2023-11-16T20:27:16.000Z"},{"Topic":"cosmos","Username":"jake\u00ae\n@jakestars_\n\u00b7\nNov 16","Tweet":"http:\/\/Stargaze.zone is your portal to the $STARS univ .....
```
