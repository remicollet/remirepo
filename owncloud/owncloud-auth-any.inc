# Apache config snippet. To be used by /etc/httpd/conf.d/*.conf files
# with Include. Allows access from any system. 

<IfModule mod_authz_core.c>
# Apache 2.4
Require all granted
</IfModule>
<IfModule !mod_authz_core.c>
# Apache 2.2
Order Deny,Allow
Allow from all
</IfModule>
