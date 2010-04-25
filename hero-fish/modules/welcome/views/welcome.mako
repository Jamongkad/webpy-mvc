<%inherit file="base.mako" />
<%def name="title()">
    Start Page
</%def>

<div class="grid_10">
<p>
    Welcome to Frontier! (name pending) Frontier is a free web based game developed by the brothers Mathew and Martie Wong. It is a based in the 
    fictional galaxy of Galacticus Seven. You either can play a space merchant who can expand his empire by setting up shop and trading for goods.
    Or try your luck playing as a space mercenary, where plying your trade by protecting merchant trade space or practice piracy and fleece your 
    victims for all their worth. 
</p>

<form method="POST" action="/pwet">
    <div>${frm.username.label}: ${frm.username()}</div>
    <div>${frm.password.label}: ${frm.password()}</div>
    <input type="submit" value="submit" />
</form>
</div>
