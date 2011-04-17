% for child in w.children:
	${child.display() | n}
% endfor
<script type="text/javascript">
  moksha_base_url = "${w.base_url}";
  moksha_csrf_token = "${w.csrf_token}";
  moksha_csrf_trusted_domains = ${w.csrf_trusted_domains};
  moksha_userid = "${w.user_id}";
  moksha_debug = ${w.debug};
  moksha_profile = ${w.profile};
</script>

