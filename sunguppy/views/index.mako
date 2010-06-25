<%inherit file="base.mako" />
<%def name="title()">
    SunGuppy!
</%def>
<div class="grid_10">
% for i in products.find():
    <div>${i['name']}</div>
% endfor
</div>
