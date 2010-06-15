<ul class='nav'>
    <li><strong>Login</strong>
        <ul>
            <li>
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
            </li>
        </ul>
    </li> 

    <li><strong>Create your account now!</strong>
        <ul>
            <li>
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
            </li>
        </ul>
    </li>
</ul>
