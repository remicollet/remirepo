# remirepo spec file for php-PHPMailer, from:
#
# Fedora spec file for php-PHPMailer
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%global github_user  PHPMailer
%global github_app   PHPMailer
%global github_tag   b18cb98131bd83103ccb26a888fdfe3177b8a663
%global github_short %(c=%{github_tag}; echo ${c:0:7})

%global		arch_name	%{github_app}-%{github_tag}

Name:		php-PHPMailer
Summary:	PHP email transport class with a lot of features
Version:	5.2.22
Release:	1%{?dist}
License:	LGPLv2+
Group:		System Environment/Libraries
URL:		http://phpmailer.worxware.com/

Source0:	https://github.com/%{github_user}/%{github_app}/archive/%{github_tag}/%{github_app}-%{version}-%{github_short}.tar.gz

# Fix language default path
# Don't rely on autoloader (for app which overides __construct)
Patch0:		%{github_app}-path.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Buildarch:	noarch

#for tests
BuildRequires: php-cli

# From phpcompatinfo report for 5.2.16
Requires:	php-date
Requires:	php-filter
Requires:	php-hash
Requires:	php-imap
Requires:	php-intl
Requires:	php-mbstring
Requires:	php-openssl
Requires:	php-pcre
Requires:	php-spl

Provides:	php-composer(phpmailer/phpmailer) = %{version}


%description
Full Featured Email Transfer Class for PHP. PHPMailer features:

    * Supports emails digitally signed with S/MIME encryption!
    * Supports emails with multiple TOs, CCs, BCCs and REPLY-TOs
    * Works on any platform.
    * Supports Text & HTML emails.
    * Embedded image support.
    * Multipart/alternative emails for mail clients that do not read
      HTML email.
    * Flexible debugging.
    * Custom mail headers.
    * Redundant SMTP servers.
    * Support for 8bit, base64, binary, and quoted-printable encoding.
    * Word wrap.
    * Multiple fs, string, and binary attachments (those from database,
      string, etc).
    * SMTP authentication.
    * Tested on multiple SMTP servers: Sendmail, qmail, Postfix, Gmail,
      Imail, Exchange, etc.
    * Good documentation, many examples included in download.
    * It's swift, small, and simple.


#-------------------------------------------------------------------------------
%prep
#-------------------------------------------------------------------------------

%setup -q -n %{arch_name}

%patch0 -p1 -b .rpm


#-------------------------------------------------------------------------------
%build
#-------------------------------------------------------------------------------

#	Make sure all file lines are \n terminated.

find . -type f -exec sed -i -e 's/[\r\t ]*$//' '{}' ';'


#-------------------------------------------------------------------------------
%install
#-------------------------------------------------------------------------------

rm -rf "${RPM_BUILD_ROOT}"

#	install directories.

install -p -d -m 755 "${RPM_BUILD_ROOT}%{_datadir}/php/PHPMailer/"
install -p -d -m 755 "${RPM_BUILD_ROOT}%{_datadir}/PHPMailer/language/"

#	Install class files.

install -p -m 644 class.*.php PHPMailerAutoload.php \
	"${RPM_BUILD_ROOT}/%{_datadir}/php/PHPMailer/"

#	Install language files (these are not gettextized).

install -p -m 644 language/*.php					\
	"${RPM_BUILD_ROOT}%{_datadir}/PHPMailer/language"

#	Tag language files.

(
	cd "${RPM_BUILD_ROOT}"
	find ".%{_datadir}/PHPMailer/language" -name "phpmailer.lang-*.php" |
		sed -e 's/^\.//'					\
		    -e 's#^.*/phpmailer\.lang-\(.*\)\.php$#%lang(\1) &#'
) > files.list


%check
: Test autoloader and version
php -r '
require "%{buildroot}%{_datadir}/php/PHPMailer/PHPMailerAutoload.php";
$mailer = new PHPMailer();
version_compare($mailer->Version, "%{version}", "=") or exit(1);
'


#-------------------------------------------------------------------------------
%clean
#-------------------------------------------------------------------------------

rm -rf "${RPM_BUILD_ROOT}"


#-------------------------------------------------------------------------------
%files -f files.list
#-------------------------------------------------------------------------------

%defattr(-, root, root, -)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc examples
%doc composer.json
%{_datadir}/php/PHPMailer
%dir %{_datadir}/PHPMailer
%dir %{_datadir}/PHPMailer/language


%changelog
* Mon Jan  9 2017 Remi Collet <remi@fedoraproject.org> - 5.2.22-1
- update to 5.2.22
- fix local file disclosure vulnerability CVE-2017-5223

* Wed Dec 28 2016 Remi Collet <remi@fedoraproject.org> - 5.2.21-1
- update to 5.2.21
- fix Remote Code Execution CVE-2016-10045

* Mon Dec 26 2016 Remi Collet <remi@fedoraproject.org> - 5.2.19-1
- update to 5.2.19

* Sun Dec 25 2016 Remi Collet <remi@fedoraproject.org> - 5.2.18-1
- update to 5.2.18
- fix Remote Code Execution CVE-2016-10033

* Fri Dec  9 2016 Remi Collet <remi@fedoraproject.org> - 5.2.17-1
- update to 5.2.17
- drop documentation removed by upstream

* Sat Jun 25 2016 Johan Cwiklinski <johan AT x-tnd DOT be> - 5.2.16-2
- add a check on version

* Mon Jun  6 2016 Remi Collet <remi@fedoraproject.org> - 5.2.16-1
- update to 5.2.16

* Wed May 11 2016 Remi Collet <remi@fedoraproject.org> - 5.2.15-1
- update to 5.2.15

* Mon Dec  7 2015 Patrick Monnerat <patrick.monnerat@dh.com> 5.2.14-1
- New upstream release: fixes CVE-2015-8476.

* Mon May  4 2015 Remi Collet <remi@fedoraproject.org> - 5.2.10-1
- update to 5.2.10

* Fri Sep 26 2014 Remi Collet <remi@fedoraproject.org> - 5.2.9-1
- update to 5.2.9

* Mon Aug 11 2014 Remi Collet <remi@fedoraproject.org> - 5.2.8-1
- update to 5.2.8
- provide php-composer(phpmailer/phpmailer)
- explicit dependencies
- fix license handling
- fix language dir using a patch instead of sed
- provide upstream autoloader

* Tue Apr 16 2013 Patrick Monnerat <pm@datasphere.ch> 5.2.6-1
- New upstream release: source moved to github.

* Wed Mar 27 2013 Remi Collet <RPMS@FamilleCollet.com> - 5.2.4-1
- Update to 5.2.4

* Mon Dec 24 2012 Remi Collet <RPMS@FamilleCollet.com> - 5.2.2-1
- Update to 5.2.2, rebuild for remi repository

* Sun Dec 23 2012 Johan Cwiklinski <johan AT x-tnd DOT be> - 5.2.2-1
- Latest upstream release

* Thu Mar 22 2012 Remi Collet <RPMS@FamilleCollet.com> - 5.2.1-1
- Update to 5.2.1, rebuild for remi repository

* Tue Mar 20 2012 Johan Cwiklinski <johan AT x-tnd DOT be> - 5.2.1-1
- Latest upstream release

* Thu Jul 21 2011 Remi Collet <RPMS@FamilleCollet.com> - 5.1.4
- rebuild for remi repository
- add BuildRoot for old version

* Mon Jul 18 2011 Patrick Monnerat <pm@datasphere.ch> 5.1-4
- Patch "sign" to fix mail signing.
  https://sourceforge.net/tracker/?func=detail&aid=3370322&group_id=26031&atid=385709

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul  8 2010 Patrick Monnerat <pm@datasphere.ch> 5.1-2
- Get rid of dos2unix build requirement and of BuildRoot rpm tag.

* Fri Jan 15 2010 Patrick Monnerat <pm@datasphere.ch> 5.1-1
- New upstream release.
- Moved endline conversion and default language path update from prep to
  build section.
- Patch "php53" to remove PHP 5.3 deprecated features.

* Mon Aug  3 2009 Patrick Monnerat <pm@datasphere.ch> 5.0.2-3
- Home page change.
- Package description from new home page.
- Requires php-mbstring.

* Fri Jun 19 2009 Patrick Monnerat <pm@datasphere.ch> 5.0.2-2
- Suppress "ed" build requirement.
- Tag language files.
- Move class files to a package-specific directory.

* Tue Jun  2 2009 Patrick Monnerat <pm@datasphere.ch> 5.0.2-1
- Initial RPM spec file.
