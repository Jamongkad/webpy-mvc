<%inherit file="base.mako" />
<%def name="title()">
    Sunguppy Welcome Page
</%def>
${header}
<div class="grid_10">
    ${user_id}
</div>

<script type="text/javascript">
jQuery(function($){
    $('#planets').asmSelect()
});
</script>
