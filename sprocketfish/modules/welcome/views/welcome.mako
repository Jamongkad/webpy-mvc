<%inherit file="base.mako" />
<%def name="title()">
    SprocketFish Welcome Page
</%def>

<div class="grid_10">
    <b>Welcome ${name}!</b>
    % if jobs:
        <p>${jobs}</p>
    % else:
        <p>No jobs.</p>
    % endif

    <form method="POST" action="/welcome/add_job">
        ${job_form.job_name()}  <br/>
        ${job_form.job_desc()} <br/>
        <input type="submit" value="add job" />
    </form>
</div>

<script type="text/javascript">
</script>
