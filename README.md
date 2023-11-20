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
<p>Keys of the output</p>

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
            <td>tweet_id</td>
            <td>String</td>
            <td>Post Identifier(integer casted inside string)</td>
        </tr>
        <tr>
            <td>username</td>
            <td>String</td>
            <td>Username of the profile</td>
        </tr>
        <tr>
            <td>name</td>
            <td>String</td>
            <td>Name of the profile</td>
        </tr>
        <tr>
            <td>replies</td>
            <td>Integer</td>
            <td>Number of replies of tweet</td>
        </tr>
        <tr>
            <td>retweets</td>
            <td>Integer</td>
            <td>Number of retweets of tweet</td>
        </tr>
        <tr>
            <td>likes</td>
            <td>Integer</td>
            <td>Number of likes of tweet</td>
        </tr>
        <tr>
            <td>is_retweet</td>
            <td>boolean</td>
            <td>Is the tweet a retweet?</td>
        </tr>
        <tr>
            <td>retweet_link</td>
            <td>String</td>
            <td>If it is retweet, then the retweet link else it'll be empty string</td>
        </tr>
        <tr>
            <td>posted_time</td>
            <td>String</td>
            <td>Time when tweet was posted in ISO 8601 format</td>
        </tr>
        <tr>
            <td>content</td>
            <td>String</td>
            <td>content of tweet as text</td>
        </tr>
        <tr>
            <td>hashtags</td>
            <td>Array</td>
            <td>Hashtags presents in tweet, if they're present in tweet</td>
        </tr>
        <tr>
            <td>tweet_url</td>
            <td>String</td>
            <td>URL of the tweet</td>
        </tr>
    </tbody>
</table>
</div>
<br>
<hr>
