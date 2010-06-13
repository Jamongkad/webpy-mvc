<%inherit file="base.mako" />
<%def name="title()">
    Frontier Welcome Page
</%def>

<div class="grid_10">
    ${user_id}
</div>

<script type="text/javascript">
jQuery(function($){
    $('#planets').asmSelect()
});
</script>
