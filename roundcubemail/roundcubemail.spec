# remirepo spec file for roundcubemail, from:

# Fedora spec file for roundcubemail
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%if 0%{?fedora} >= 21
# support for apache / nginx / php-fpm
%global with_phpfpm 1
%else
%global with_phpfpm 0
%endif
#global prever      rc

%global roundcubedir %{_datadir}/roundcubemail
%global _logdir /var/log  
Name: roundcubemail
Version:  1.2.3
Release:  1%{?dist}
Summary: Round Cube Webmail is a browser-based multilingual IMAP client

Group: Applications/System
# Since 0.8 beta, the main code has been GPLv3+ with exceptions and
# skins CC-BY-SA.
# Plugins are a mix of GPLv3+ and GPLv2. The Enigma plugin contains a
# copy of php-Pear-Crypt-GPG (not yet packaged for Fedora), which is
# LGPLv2+. The jqueryui plugin contains the entire jQuery UI framework
# for the use of roundcube plugins: it is licensed as MIT or GPLv2.
# The program/js/tiny_mce directory contains an entire copy of TinyMCE
# which is LGPLv2+.
# https://github.com/pear/Crypt_GPG
# http://jqueryui.com/
# http://www.tinymce.com/
License: GPLv3+ with exceptions and GPLv3+ and GPLv2 and LGPLv2+ and CC-BY-SA and (MIT or GPLv2)
URL: http://www.roundcube.net
Source0: https://github.com/roundcube/roundcubemail/releases/download/%{version}%{?prever:-%{prever}}/roundcubemail-%{version}%{?prever:-%{prever}}.tar.gz

Source1: roundcubemail.httpd
Source3: roundcubemail.nginx
Source2: roundcubemail.logrotate
Source4: roundcubemail-README.rpm
# Elegantly handle removal of moxieplayer Flash binary in tinymce
# media plugin (see "Drop precompiled flash" in %%prep)
Patch0: roundcubemail-1.2.1-no_swf.patch

# Non-upstreamable: Adjusts config path to Fedora policy
Patch1: roundcubemail-1.2.1-confpath.patch

# add .log prefix to all log file names
# see https://github.com/roundcube/roundcubemail/pull/313
Patch2: roundcubemail-pr313.patch

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root%(%{__id_u} -n)
%if %{with_phpfpm}
Requires:  webserver
Requires:  nginx-filesystem
Requires:  httpd-filesystem
Requires:  php(httpd)
%else
Requires: httpd
Requires: mod_php
%endif
Requires: php-curl
Requires: php-date
Requires: php-dom
Requires: php-fileinfo
Requires: php-gd
Requires: php-hash
Requires: php-iconv
Requires: php-intl
Requires: php-json
Requires: php-ldap
Requires: php-mbstring
Requires: php-openssl
Requires: php-pcre
Requires: php-posix
Requires: php-pdo
Requires: php-pspell
Requires: php-session
Requires: php-simplexml
Requires: php-sockets
Requires: php-spl
Requires: php-xml
# From composer.json-dist, require
#        "php": ">=5.3.7",
#        "pear/pear-core-minimal": "~1.10.1",
#        "roundcube/plugin-installer": "~0.1.6",
#        "pear-pear.php.net/net_socket": "~1.0.12",
#        "pear-pear.php.net/auth_sasl": "~1.0.6",
#        "pear-pear.php.net/net_idna2": "~0.1.1",
#        "pear-pear.php.net/mail_mime": "~1.10.0",
#        "pear-pear.php.net/net_smtp": "~1.7.1",
#        "pear-pear.php.net/crypt_gpg": "~1.4.1",
#        "roundcube/net_sieve": "~1.5.0"
#   not available and doesn't make sense roundcube/plugin-installer
Requires: php-pear(PEAR)            >= 1.10.1
Requires: php-pear(Net_Socket)      >= 1.0.12
Requires: php-pear(Auth_SASL)       >= 1.0.6
Requires: php-pear(Net_IDNA2)       >= 0.1.1
Requires: php-pear(Mail_Mime)       >= 1.10.0
Requires: php-pear(Net_SMTP)        >= 1.7.1
Requires: php-pear(Crypt_GPG)       >= 1.4.2
Requires: php-composer(roundcube/net_sieve) >= 1.5.0
# From composer.json-dist, suggest
#        "pear-pear.php.net/net_ldap2": "~2.2.0 required for connecting to LDAP address books",
#        "kolab/Net_LDAP3": "dev-master required for connecting to LDAP address books"
Requires: php-pear(Net_LDAP2)       >= 2.2.0
Requires: php-composer(kolab/Net_LDAP3)
# mailcap for /etc/mime.types
Requires: mailcap

# Optional deps
# Spell check
#Suggests: php-enchant
# Caching
#Suggests: php-apc
#Suggests: php-memcache
# EXIF images
Requires: php-exif
# Upload progress (shock!)
#Suggests: php-uploadprogress
# ZIP download plugin
Requires: php-zip

# Gearman support
#Optional: php-gearman
# PAM password support
#Optional: php-pam


%description
RoundCube Webmail is a browser-based multilingual IMAP client
with an application-like user interface. It provides full
functionality you expect from an e-mail client, including MIME
support, address book, folder manipulation, message searching
and spell checking. RoundCube Webmail is written in PHP and 
requires a database: MySQL, PostgreSQL and SQLite are known to
work. The user interface is fully skinnable using XHTML and
CSS 2.


%prep
%setup -q -n roundcubemail-%{version}%{?prever:-%{prever}}
%patch0 -p1
%patch1 -p1
%patch2 -p1

# fix permissions and remove any .htaccess files
find . -type f -print | xargs chmod a-x
find . -name \.htaccess -print | xargs rm -f

# Fix shebang
chmod +x bin/*sh
sed -e '/^#!/s:/usr/bin/env php:/usr/bin/php:' \
    -i bin/*sh

# ??? - Jon, this could do with a comment; fixing carriage returns? (adamw)
sed -i 's/\r//' SQL/mssql.initial.sql

# Drop precompiled flash
find . -type f -name '*.swf'  -exec rm {} \; -print

# drop file from patch
find . -type f -name '*.orig' -exec rm {} \; -print

# Wipe bbcode plugin from bundled TinyMCE to make doubleplus sure we cannot
# be vulnerable to CVE-2012-4230, unaddressed upstream
echo "CVE-2012-4230: removing tinymce bbcode plugin, check path if this fails."
test -d program/js/*mce/plugins/bbcode && rm -rf program/js/*mce/plugins/bbcode || exit 1

# Create simple autoloader for PEAR
mkdir vendor
cat << EOF | tee vendor/autoload.php
<?php
spl_autoload_register(
	function (\$class) {
		if (strpos(\$class, '.') === false) {
			\$file = str_replace('_', '/', \$class).'.php';
			if (\$path = stream_resolve_include_path(\$file)) {
				require_once(\$path);
			}
		}
	}
);
EOF


%build
# Nothing


%install
rm -rf %{buildroot}
install -d %{buildroot}%{roundcubedir}
cp -pr * %{buildroot}%{roundcubedir}

# Apache with mod_php or php-fpm
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf

%if %{with_phpfpm}
# Nginx with php-fpm
install -Dpm 0644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/nginx/default.d/%{name}.conf
%endif

mkdir -p %{buildroot}%{_sysconfdir}/roundcubemail
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
cp -pr %SOURCE2 %{buildroot}%{_sysconfdir}/logrotate.d/roundcubemail

%if 0%{?rhel} == 5 || 0%{?rhel} == 6
: Remove "su" option from logrotate configuration file - requires logrotate 3.8+
sed -e '/su /d' -i %{buildroot}%{_sysconfdir}/logrotate.d/roundcubemail
%endif

# Log files
mkdir -p %{buildroot}/var/log/roundcubemail
# Temp files
mkdir -p %{buildroot}/var/lib/roundcubemail/temp
# GPG keys
mkdir -p %{buildroot}/var/lib/roundcubemail/enigma

cp -pr %SOURCE4 README.rpm

# create empty files for ghost to not remove OLD config (0.9.x)
touch %{buildroot}%{_sysconfdir}/roundcubemail/db.inc.php
touch %{buildroot}%{_sysconfdir}/roundcubemail/main.inc.php
# create empty files for ghost for the NEW config
touch %{buildroot}%{_sysconfdir}/roundcubemail/config.inc.php

# keep any other config files too
mv %{buildroot}%{roundcubedir}/config/* %{buildroot}%{_sysconfdir}/roundcubemail/

# Also move plugins configuration file samples
pushd %{buildroot}%{roundcubedir}/plugins
for plug in $(ls); do
  if [ -f $plug/config.inc.php.dist ]; then
    mv $plug/config.inc.php.dist %{buildroot}%{_sysconfdir}/roundcubemail/$plug.inc.php.dist
  fi
done
popd

# clean up the buildroot
rm -r %{buildroot}%{roundcubedir}/{config,logs,temp}
rm -r %{buildroot}%{roundcubedir}/{CHANGELOG,INSTALL,LICENSE,README.md,UPGRADING}
rm    %{buildroot}%{roundcubedir}/composer.json-dist


%pre
# Drop some old config options to ensure new defaults are used
if [ -f %{_sysconfdir}/%{name}/main.inc.php ]; then
  sed -e "/'temp_dir'/d" \
      -e "/'mime_types'/d" \
      -e "/'log_dir'/d" \
      -i %{_sysconfdir}/%{name}/main.inc.php
fi


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CHANGELOG INSTALL README.md UPGRADING README.rpm
%doc composer.json-dist
%{roundcubedir}
%dir %{_sysconfdir}/%{name}
# OLD config files from previous version
%ghost %attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/%{name}/db.inc.php
%ghost %attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/%{name}/main.inc.php
# NEW config file
%ghost %attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/%{name}/config.inc.php
# Default upstream values, overwritten on update
%attr(0640,root,apache) %{_sysconfdir}/%{name}/mimetypes.php
%attr(0640,root,apache) %{_sysconfdir}/%{name}/defaults.inc.php
%attr(0640,root,apache) %{_sysconfdir}/%{name}/config.inc.php.sample
%attr(0640,root,apache) %{_sysconfdir}/%{name}/*.inc.php.dist
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%if %{with_phpfpm}
%config(noreplace) %{_sysconfdir}/nginx/default.d/%{name}.conf
%endif
%attr(0770,root,apache) %dir /var/log/roundcubemail
%attr(0770,root,apache) %dir /var/lib/roundcubemail
%attr(0770,root,apache) %dir /var/lib/roundcubemail/temp
%attr(0770,root,apache) %dir /var/lib/roundcubemail/enigma
%config(noreplace) %{_sysconfdir}/logrotate.d/roundcubemail


%changelog
* Tue Nov 29 2016 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- update to 1.2.3

* Thu Sep 29 2016 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- update to 1.2.2

* Sun Jul 31 2016 Remi Collet <remi@fedoraproject.org> - 1.2.1-3
- use /var/lib/roundcubemail/temp for temporary files
- add /var/lib/roundcubemail/enigma for GPG keys storage
- move plugins configuration samples in /etc/roundcubemail
- fix permission adjustments required for encryption support #1347332

* Wed Jul 27 2016 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- update to 1.2.1

* Fri May 27 2016 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0
- raise dependency on Crypt_GPG ~1.4.1

* Thu Apr 21 2016 Remi Collet <remi@fedoraproject.org> - 1.2-0.2.rc
- update to 1.2-rc
- sources from github
- raise dependency on Net_LDAP2 >= 2.2.0
- add dependency on Net_Socket >= 1.0.12

* Mon Dec 28 2015 Remi Collet <remi@fedoraproject.org> - 1.2-0.1.beta
- update to 1.2-beta
- raise dependency to Mail_Mime ~1.10.0
- add dependency on roundcube/net_sieve ~1.5.0
- add dependency on Crypt_GPG ~1.4.0

* Mon Dec 28 2015 Remi Collet <remi@fedoraproject.org> - 1.1.4-2
- add .log suffix to all log files, and rotate all #1269164
- more secure permissions on /var/log and /var/lib #1269155

* Sun Dec 27 2015 Remi Collet <remi@fedoraproject.org> - 1.1.4-1
- update to 1.1.4
- raise dependency on Net_SMTP 1.7.1

* Tue Sep 15 2015 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- update to 1.1.3
- raise dependencies on Mail_Mime 1.9.0, Net_Sieve 1.3.4,
  Net_SMTP 1.6.3
- drop dependency on Mail_mimeDecode

* Tue Aug 11 2015 Remi Collet <remi@fedoraproject.org> - 1.1.2-2
- Remove "su" option from logrotate configuration file (requires
  logrotate >= 3.8.0) to avoid daily logrotate errors with old RHEL

* Fri Jun  5 2015 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- update to 1.1.2

* Wed Mar 25 2015 Robert Scheck <robert@fedoraproject.org> - 1.1.1-2
- switch run-time requirement from php-mcrypt to php-openssl

* Fri Mar 20 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- update to 1.1.1

* Sun Feb 22 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-2
- add optional dependencies for LDAP management on
  Net_LDAP2 and Net_LDAP3

* Mon Feb 16 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to 1.1.0

* Sun Jan 25 2015 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5 (security update)

* Sun Dec 21 2014 Remi Collet <remi@fedoraproject.org> - 1.0.4-3
- provide Nginx configuration

* Sat Dec 20 2014 Adam Williamson <awilliam@redhat.com> - 1.0.4-2
- drop tinymce bbcode plugin for safety (CVE-2012-4230)

* Fri Dec 19 2014 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4 (service release, security)

* Tue Sep 30 2014 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3 (service release)

* Tue Jul 22 2014 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2 (service release)
- pull README change from rawhide

* Mon Jul 21 2014 Adam Williamson <awilliam@redhat.com> - 1.0.2-1
- Update to 1.0.2

* Mon May 12 2014 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1 (service release)

* Thu May  8 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- cleanup some config option from previous version
- requires mailcap for /etc/mime.types

* Thu May  8 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0
- provide the installer

* Tue Oct 22 2013 Remi Collet <remi@fedoraproject.org> - 0.9.5-1
- backport 0.9.5 for remi repo

* Tue Oct 22 2013 Jon Ciesla <limburgher@gmail.com> - 0.9.5-1
- Fix for CVE-2013-6172, BZ 1021735, 1021965.

* Mon Sep 09 2013 Jon Ciesla <limburgher@gmail.com> - 0.9.4-1
- 0.9.4
- Change httpd dep to webserver, BZ 1005696.

* Sat Aug 24 2013 Remi Collet <remi@fedoraproject.org> - 0.9.3-2
- sync with rawhide for remi repo

* Fri Aug 23 2013 Adam Williamson <awilliam@redhat.com> - 0.9.3-2
- patch tinymce to cope elegantly with Flash binary being removed

* Fri Aug 23 2013 Remi Collet <remi@fedoraproject.org> - 0.9.3-1
- backport 0.9.3 for remi repo in sync with rawhide

* Fri Aug 23 2013 Jon Ciesla <limburgher@gmail.com> - 0.9.3-1
- Fix two XSS vulnerabilities:
- http://trac.roundcube.net/ticket/1489251

* Fri Aug 16 2013 Jon Ciesla <limburgher@gmail.com> - 0.9.2-3
- Drop precompiled flash.

* Tue Jun 18 2013 Remi Collet <remi@fedoraproject.org> - 0.9.1-1
- backport 0.9.2 for remi repo in sync with rawhide

* Mon Jun 17 2013 Adam Williamson <awilliam@redhat.com> - 0.9.2-1
- latest upstream
- correct License field, add comment on complex licensing case

* Sat May  4 2013 Remi Collet <remi@fedoraproject.org> - 0.9.0-1
- backport 0.9.0 for remi repo in sync with rawhide

* Wed May 01 2013 Adam Williamson <awilliam@redhat.com> - 0.9.0-1
- latest upstream
- drop MDB2 dependencies, add php-pdo dependency (upstream now using
  pdo not MDB2)
- drop the update.sh script as it requires the installer framework we
  don't ship
- update the Fedora README for changes to sqlite and update process
- drop strict.patch, upstream actually merged it years ago, just in
  a slightly different format, and we kept dumbly diffing it
- drop references to obsolete patches (all merged upstream long ago)

* Thu Mar 28 2013 Remi Collet <remi@fedoraproject.org> - 0.8.6-1
- backport 0.8.6 for remi repo

* Thu Mar 28 2013 Jon Ciesla <limburgher@gmail.com> - 0.8.6-1
- Latest upstream, fixes local file inclusion via web UI
- modification of certain config options.

* Fri Feb 08 2013 Remi Collet <remi@fedoraproject.org> - 0.8.5-1
- Latest upstream, CVE-2012-6121, backport for remi repo

* Fri Feb 08 2013 Jon Ciesla <limburgher@gmail.com> - 0.8.5-1
- Latest upstream, CVE-2012-6121.

* Mon Jan 21 2013 Remi Collet <remi@fedoraproject.org> - 0.8.4-3
- fix configuration for httpd 2.4 (missing in backport)

* Mon Dec 03 2012 Remi Collet <remi@fedoraproject.org> - 0.8.4-2
- improved Requires

* Mon Nov 19 2012 Jon Ciesla <limburgher@gmail.com> - 0.8.4-1
- Latest upstream.

* Fri Nov 16 2012 Remi Collet <remi@fedoraproject.org> - 0.8.4-1
- new upstream release 0.8.4

* Mon Oct 29 2012 Remi Collet <remi@fedoraproject.org> - 0.8.2-3
- fix configuration for httpd 2.4 (#871123)

* Sun Oct 28 2012 Remi Collet <remi@fedoraproject.org> - 0.8.2-2
- add fix for latest MDB2 (#870933)

* Wed Oct 10 2012 Jon Ciesla <limburgher@gmail.com> - 0.8.2-1
- Latest upstream.

* Thu Aug 30 2012 Adam Williamson <awilliam@redhat.com> - 0.8.1-2
- correct stray parenthesis in strict patch

* Mon Aug 20 2012 Jon Ciesla <limburgher@gmail.com> - 0.8.1-1
- Latest upstream.
- Updated strict patch.
- XSS patch upstreamed.

* Mon Aug 20 2012 Jon Ciesla <limburgher@gmail.com> - 0.7.3-1
- 0.7.3, patch for XSS in signature issue, BZ 849616, 849617.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 12 2012 Jon Ciesla <limburgher@gmail.com> - 0.7.2-2
- Rediffed strict patch.

* Mon Mar 12 2012 Adam Williamson <awilliam@redhat.com> - 0.7.2-1
- new upstream release 0.7.2

* Thu Feb 16 2012 Jon Ciesla <limburgher@gmail.com> - 0.7.1-2
- Fix logrotate, BZ 789552.
- Modify error logging for strict, BZ 789576.

* Wed Feb  1 2012 Adam Williamson <awilliam@redhat.com> - 0.7.1-1
- new upstream release

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 14 2011 Adam Williamson <awilliam@redhat.com> - 0.7-1
- new upstream release
- drop all patches except confpath.patch:
	+ html2text.patch and all CVE fixes were merged upstream
	+ pg-mdb2.patch no longer necessary as all currently supported
	  Fedora releases have a php-pear-MDB2-Driver-pgsql package new
	  enough to work with this option

* Fri Oct 07 2011 Jon Ciesla <limb@jcomserv.net> = 0.6-1
- New upstream.

* Tue Sep 06 2011 Jon Ciesla <limb@jcomserv.net> = 0.5.4-1
- New upstream, fixes multiple security issues.

* Tue Jul 05 2011 Jon Ciesla <limb@jcomserv.net> = 0.5.3-1
- New upstream.

* Tue May 17 2011 Jon Ciesla <limb@jcomserv.net> = 0.5.2-1
- New upstream.

* Thu Feb 10 2011 Jon Ciesla <limb@jcomserv.net> = 0.5.1-1
- New upstream.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 18 2010 Jon Ciesla <limb@jcomserv.net> = 0.4.2-1
- New upstream.

* Mon Oct 04 2010 Jon Ciesla <limb@jcomserv.net> = 0.4.1-1
- New upstream.

* Mon Feb 01 2010 Jon Ciesla <limb@jcomserv.net> = 0.3.1-2
- Patch to fix CVE-2010-0464, BZ 560143.

* Mon Nov 30 2009 Jon Ciesla <limb@jcomserv.net> = 0.3.1-1
- New upstream.

* Thu Oct 22 2009 Jon Ciesla <limb@jcomserv.net> = 0.3-2
- Macro fix, BZ530037.

* Wed Sep 23 2009 Jon Ciesla <limb@jcomserv.net> = 0.3-1
- New upstream.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Jon Ciesla <limb@jcomserv.net> = 0.2.2-2
- Incorporated Chris Eveleigh's config changes to fix mimetype bug, BZ 511857.

* Wed Jul 01 2009 Jon Ciesla <limb@jcomserv.net> = 0.2.2-1
- New upstream.

* Fri Apr 10 2009 Jon Ciesla <limb@jcomserv.net> = 0.2.1-1
- New upstream.

* Mon Mar 30 2009 Jon Ciesla <limb@jcomserv.net> = 0.2-9.stable
- Patch for PG until php-pear-MDB2 hits 1.5.0 stable. BZ 489505.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-8.stable
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 04 2009 Jon Ciesla <limb@jcomserv.net> = 0.2-7.stable
- Patch for CVE-2009-0413, BZ 484052.

* Mon Jan 05 2009 Jon Ciesla <limb@jcomserv.net> = 0.2-6.stable
- New upstream.
- Dropped two most recent patches, applied upstream.

* Wed Dec 17 2008 Jon Ciesla <limb@jcomserv.net> = 0.2-5.beta
- Security fix, BZ 476830.

* Fri Dec 12 2008 Jon Ciesla <limb@jcomserv.net> = 0.2-4.beta
- Security fix, BZ 476223.

* Thu Oct 09 2008 Jon Ciesla <limb@jcomserv.net> = 0.2-3.beta
- New upstream.

* Mon Jun 16 2008 Jon Ciesla <limb@jcomserv.net> = 0.2-2.alpha
- osx files removed upstream.

* Mon Jun 16 2008 Jon Ciesla <limb@jcomserv.net> = 0.2-1.alpha
- Fixed php-xml, php-mbstring Requires.  BZ 451652.
- Removing osx files, will be pulled from next upstream release.

* Fri Jun 13 2008 Jon Ciesla <limb@jcomserv.net> = 0.2-0.alpha
- Update to 0.2-alpha, security fixes for BZ 423271. 
- mysql update and pear patches applied upstream.
- Patched config paths.

* Fri Apr 18 2008 Jon Ciesla <limb@jcomserv.net> = 0.1.1-5
- Added php-pecl-Fileinfo Reqires. BZ 442728.

* Wed Apr 16 2008 Jon Ciesla <limb@jcomserv.net> = 0.1.1-4
- Added mcrypt, MDB2 Requires.  BZ 442728.

* Thu Apr 10 2008 Jon Ciesla <limb@jcomserv.net> = 0.1.1-3
- Patch to fix PEAR path issue, drop symlinks.

* Thu Apr 10 2008 Jon Ciesla <limb@jcomserv.net> = 0.1.1-2
- Drop %%pre script that was breaking pear packages.

* Wed Apr 09 2008 Jon Ciesla <limb@jcomserv.net> = 0.1.1-1
- New upstream release.
- Added patch to fix mysql update.

* Tue Mar 18 2008 Jon Ciesla <limb@jcomserv.net> = 0.1-1
- Updgrade to 0.1 final, -dep.
- Added new mimeDecode dep.

* Mon Feb 04 2008 Jon Ciesla <limb@jcomserv.net> = 0.1-0.10rc2.1
- Changed to upstream -dep tarball, GPL-compliant.

* Fri Feb 01 2008 Jon Ciesla <limb@jcomserv.net> = 0.1-0.9rc2.1
- re-removed PEAR components that slipped back in after rc1.

* Fri Oct 26 2007 Jon Ciesla <limb@jcomserv.net> = 0.1-0.8rc2
- Upgrade to 0.1-rc2

* Thu Aug 16 2007 Jon Ciesla <limb@jcomserv.net> = 0.1-0.7rc1.1
- License tag correction.

* Tue Jul 03 2007 Jon Ciesla <limb@jcomserv.net> = 0.1-0.6rc1.1
- New upstream release, all GPL, all current languages included.

* Mon May 14 2007 Jon Ciesla <limb@jcomserv.net> = 0.1-0.5.beta2.2
- Fixed source timestamps, added Russian langpack.
- Added logpath fix to main.inc.php
- Fixed logrotate filename.

* Fri May 11 2007 Jon Ciesla <limb@jcomserv.net> = 0.1-0.4.beta2.2
- Cleanup/elegantization of spec, .conf.

* Thu May 10 2007 Jon Ciesla <limb@jcomserv.net> = 0.1-0.3.beta2.2
- Fixed bad chars in script.

* Thu May 10 2007 Jon Ciesla <limb@jcomserv.net> = 0.1-0.2.beta2.2
- Added all langpacks.

* Thu May 10 2007 Jon Ciesla <limb@jcomserv.net> = 0.1-0.1.beta2.2
- Versioning fix.

* Wed May 09 2007 Jon Ciesla <limb@jcomserv.net> = 0.1-beta2.3
- Fixed generation of DES.
- Cleanup re patch.

* Mon May 07 2007 Jon Ciesla <limb@jcomserv.net> - 0.1-beta2.2.3
- Removed duplicate docs.
- Moved SQL to doc.
- Fixed perms on log dir, sysconfdir.
- Fixed Requires.  
- Fixed config.
- Fixed changelog spacing.
  
* Fri May 04 2007 Jon Ciesla <limb@jcomserv.net> - 0.1-beta2.2.2
- Created new source tarball with PEAR code removed. Added script for creation.

* Tue Feb 13 2007 Jon Ciesla <limb@jcomserv.net> - 0.1-beta2.2.1
- Excluded Portions from PEAR, included as dependancies
- Fixed log/temp issues, including logrotate

* Tue Jan 30 2007 Jon Ciesla <limb@jcomserv.net> - 0.1-beta2.2
- Initial packaging.
