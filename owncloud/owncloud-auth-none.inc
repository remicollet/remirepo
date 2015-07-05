# Apache config snippet. To be used by /etc/httpd/conf.d/*.conf files
# with Include. Denies all access.

<IfModule mod_authz_core.c>
# Apache 2.4
Require all denied
</IfModule>
<IfModule !mod_authz_core.c>
# Apache 2.2
Order Deny,Allow
Deny from all
</IfModule>
