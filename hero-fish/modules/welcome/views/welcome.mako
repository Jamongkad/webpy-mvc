<%inherit file="base.mako" />
<%def name="title()">
    Frontier Welcome Page
</%def>

<div class="grid_10">
<form method="POST" action="/welcome/add_info">
    <select id="planets" multiple="multiple" name="planets">
        % for i in planets:
            <option value="${i['name']}">${i['name']}</option>
        % endfor
    </select>
    <input type="hidden" name="user_name" value="${user_id}" />
    <input type="submit" value="submit"/>
</form>
</div>

<script type="text/javascript">
jQuery(function($){
    $('#planets').asmSelect()
});
</script>
