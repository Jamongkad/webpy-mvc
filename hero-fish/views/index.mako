<%inherit file="base.mako" />
<%def name="title()">
    Mathew
</%def>

<p>I love Python</p>
<form action="/login" method="post">
    <p><input type="text" name="user_name"/></p>
    <p><input type="password" name="password"/></p>
    <input type="submit" value="login" />
</form>
<a href="/session_active">Next</a>
