# Apache config snippet. To be used by /etc/httpd/conf.d/*.conf files
# with Include. Allows access only from local system.

<IfModule mod_authz_core.c>
# Apache 2.4
Require local
</IfModule>
<IfModule !mod_authz_core.c>
# Apache 2.2
Order Deny,Allow
Deny from all
Allow from 127.0.0.1
Allow from ::1
</IfModule>
