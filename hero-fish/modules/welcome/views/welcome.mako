<%inherit file="base.mako" />
<%def name="title()">
    Start Page
</%def>

<div class="grid_10">
<p>
<b>Create your account now!</b>
<form method="POST" action="./create_account">
    % if frm.username.errors:
        % for error in frm.username.errors:
        <b>${error}</b>
        % endfor
    % endif
    <div>${frm.username.label}: ${frm.username()}</div>

    % if frm.password.errors:
        % for error in frm.password.errors:
        <b>${error}</b>
        % endfor
    % endif
    <div>${frm.password.label}: ${frm.password()}</div>
    <input type="submit" value="submit" />
</form>

</p>
</div>
