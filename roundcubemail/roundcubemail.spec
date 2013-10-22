%define roundcubedir %{_datadir}/roundcubemail
%global _logdir /var/log  
Name: roundcubemail
Version:  0.9.5
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
Source0: http://downloads.sourceforge.net/roundcubemail/roundcubemail-%{version}-dep.tar.gz
Source1: roundcubemail.conf
Source2: roundcubemail.logrotate
Source4: roundcubemail-README.fedora
# Elegantly handle removal of moxieplayer Flash binary in tinymce
# media plugin (see "Drop precompiled flash" in %pre)
Patch0: roundcubemail-0.9.3-no_swf.patch

# Non-upstreamable: Adjusts config path to Fedora policy
Patch6: roundcubemail-0.9.0-confpath.patch

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root%(%{__id_u} -n)
Requires: httpd
Requires: mod_php
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
Requires: php-mcrypt
Requires: php-mysql
Requires: php-pcre
Requires: php-posix
Requires: php-pdo
Requires: php-pspell
Requires: php-session
Requires: php-simplexml
Requires: php-sockets
Requires: php-spl
Requires: php-xml
Requires: php-pear(Auth_SASL)
Requires: php-pear(Mail_Mime)
Requires: php-pear(Net_SMTP)
Requires: php-pear(Net_Socket)
Requires: php-pear(Mail_mimeDecode)
Requires: php-pear(Net_IDNA2)

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
%setup -q -n roundcubemail-%{version}-dep
%patch0 -p1
%patch6 -p1

# fix permissions and remove any .htaccess files
find . -type f -print | xargs chmod a-x
find . -name \.htaccess -print | xargs rm -f

# fixup paths to use the right paths
sed -i 's|temp/|${_tmppath}|' config/main.inc.php.dist
sed -i 's|config/|%{_sysconfdir}/roundcubemail/|' config/main.inc.php.dist
sed -i 's|logs/|%{_logdir}/roundcubemail/|' config/main.inc.php.dist

# ??? - Jon, this could do with a comment; fixing carriage returns? (adamw)
sed -i 's/\r//' SQL/mssql.initial.sql

#Drop precompiled flash
find . -type f -name '*.swf' | xargs rm -f

%build

%install

rm -rf %{buildroot}
install -d %{buildroot}%{roundcubedir}
cp -pr * %{buildroot}%{roundcubedir}

#ln -s ../../../pear/PEAR.php %{buildroot}%{roundcubedir}/program/lib/PEAR.php
#ln -s ../../../pear/Auth %{buildroot}%{roundcubedir}/program/lib/Auth
#ln -s ../../../pear/DB %{buildroot}%{roundcubedir}/program/lib/DB
#ln -s ../../../pear/DB.php %{buildroot}%{roundcubedir}/program/lib/DB.php
#ln -s ../../../pear/Mail %{buildroot}%{roundcubedir}/program/lib/Mail
#ln -s ../../../pear/Net %{buildroot}%{roundcubedir}/program/lib/Net

# drop the installer and the update.sh script which depends on it
rm -rf %{buildroot}%{roundcubedir}/installer
rm -f %{buildroot}%{roundcubedir}/bin/update.sh

mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
cp -pr %SOURCE1 %{buildroot}%{_sysconfdir}/httpd/conf.d

mkdir -p %{buildroot}%{_sysconfdir}/roundcubemail
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
cp -pr %SOURCE2 %{buildroot}%{_sysconfdir}/logrotate.d/roundcubemail

mkdir -p %{buildroot}/var/log/roundcubemail

cp -pr %SOURCE4 .

# use dist files as config files
mv %{buildroot}%{roundcubedir}/config/db.inc.php.dist %{buildroot}%{_sysconfdir}/roundcubemail/db.inc.php
mv %{buildroot}%{roundcubedir}/config/main.inc.php.dist %{buildroot}%{_sysconfdir}/roundcubemail/main.inc.php
# keep any other config files too
mv %{buildroot}%{roundcubedir}/config/* %{buildroot}%{_sysconfdir}/roundcubemail/

# clean up the buildroot
rm -rf %{buildroot}%{roundcubedir}/{config,logs,temp}
rm -rf %{buildroot}%{roundcubedir}/{CHANGELOG,INSTALL,LICENSE,README,UPGRADING,SQL}

%clean
rm -rf %{buildroot}

%post
# replace default des string in config file for better security
function makedesstr
(
chars=(0 1 2 3 4 5 6 7 8 9 a b c d e f g h i j k l m n o p q r s t u v w x y z A
B C D E F G H I J K L M N O P Q R S T U V W X Y Z)

max=${#chars[*]}

for i in `seq 1 24`; do
    let rand=${RANDOM}%%${max}
    str="${str}${chars[$rand]}"
done
echo $str
)

sed -i "s/rcmail-\!24ByteDESkey\*Str/`makedesstr`/" /etc/roundcubemail/main.inc.php || : &> /dev/null
exit 0


%files
%defattr(-,root,root,-)
%doc CHANGELOG INSTALL LICENSE README.md UPGRADING SQL roundcubemail-README.fedora
%{roundcubedir}
%dir %{_sysconfdir}/%{name}
%attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/%{name}/db.inc.php
%attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/%{name}/main.inc.php
%attr(0640,root,apache) %{_sysconfdir}/%{name}/mimetypes.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/roundcubemail.conf
%attr(0775,root,apache) %dir /var/log/roundcubemail
%config(noreplace) %{_sysconfdir}/logrotate.d/roundcubemail

%changelog
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
