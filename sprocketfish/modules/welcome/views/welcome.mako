<%inherit file="base.mako" />
<%def name="title()">
    SprocketFish Welcome Page
</%def>

<div class="grid_10">
    <b>Welcome ${name}!</b>
    % if jobs:
        % for rows in jobs:
            <p>
                <b>${rows.job_nm}</b>
                <%! from datetime import date %> 
                <b>${date.fromtimestamp(float(rows.job_date_start))}</b>
            </p>
        % endfor
    % else:
        <p>No jobs.</p>
    % endif

    <form method="POST" action="/welcome/add_job">
        % if job_form.job_name.errors:
            % for i in job_form.job_name.errors:
                <b>${i}</b><br/>
            % endfor 
        % endif

        Name* <br/>${job_form.job_name()}  <br/>

        Date And Time <br/><input type="text" name="start_date" value="" class="date-pick"/></br/>

        % if job_form.job_desc.errors:
            % for i in job_form.job_desc.errors:
                <b>${i}</b><br/>
            % endfor 
        % endif
        Description* <br/>${job_form.job_desc()} <br/>
        <input type="submit" value="add job" />
    </form>
</div>

<script type="text/javascript">
    jQuery(function($) {
        $('.date-pick').datePicker()
    })
</script>
