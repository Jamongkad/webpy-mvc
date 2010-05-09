<%inherit file="base.mako" />
<%def name="title()">
    Frontier! the Space exploration game powered by it's economy!
</%def>

<div class="grid_10">
    <p>
    <b>Login</b>

    <form method="POST" action="/login">
        % if login.username.errors:
            % for error in login.username.errors:
            <b>${error}</b>
            % endfor
        % endif
        <div>${login.username.label}: ${login.username()}</div>

        % if login.password.errors:
            % for error in login.password.errors:
            <b>${error}</b>
            % endfor
        % endif
        <div>${login.password.label}: ${login.password()}</div>
        <input type="submit" value="submit" />
    </form>

    </p>
    <br/> <br/> 
    <p>
    <b>Create your account now!</b>
    <form method="POST" action="/create_account">
        % if create.username.errors:
            % for error in create.username.errors:
            <b>${error}</b>
            % endfor
        % endif
        <div>${create.username.label}: ${create.username()}</div>

        % if create.password.errors:
            % for error in create.password.errors:
            <b>${error}</b>
            % endfor
        % endif
        <div>${create.password.label}: ${create.password()}</div>
        <input type="submit" value="submit" />
    </form>

    </p>
</div>
