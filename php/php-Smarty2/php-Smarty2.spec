# remirepo spec file for php-Smarty2 from:
#
# Fedora spec file for php-Smarty2
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global gh_commit    c5c9d6514ceaf15fe35345886668726829560f93
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     smarty-php
%global gh_project   smarty

Name:           php-Smarty2
Summary:        Template/Presentation Framework for PHP
Version:        2.6.30
Release:        1%{?dist}

URL:            http://www.smarty.net
License:        LGPLv2+
Group:          Development/Libraries
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  %{_bindir}/phpab
# For tests
BuildRequires:  php-cli

# From composer.json
Requires:       php(language) >= 5.2
# From phpcompatinfo report for 2.6.30
Requires:       php-date
Requires:       php-pcre

Provides:       php-composer(smarty/smarty) = %{version}


%description
Although Smarty is known as a "Template Engine", it would be more accurately
described as a "Template/Presentation Framework." That is, it provides the
programmer and template designer with a wealth of tools to automate tasks
commonly dealt with at the presentation layer of an application. I stress the
word Framework because Smarty is not a simple tag-replacing template engine.
Although it can be used for such a simple purpose, its focus is on quick and
painless development and deployment of your application, while maintaining
high-performance, scalability, security and future growth.

Autoloader: %{_datadir}/php/Smarty2/autoload.php


%prep
%setup -qn %{gh_project}-%{gh_commit}
iconv -f iso8859-1 -t utf-8 NEWS > NEWS.conv && mv -f NEWS.conv NEWS
iconv -f iso8859-1 -t utf-8 ChangeLog > ChangeLog.conv && mv -f ChangeLog.conv ChangeLog

%{_bindir}/phpab \
   --output libs/autoload.php \
   libs/Smarty.class.php  libs/Smarty_Compiler.class.php libs/Config_File.class.php


%build
# empty build section, nothing required


%install
rm -rf $RPM_BUILD_ROOT

# install smarty libs
install -d $RPM_BUILD_ROOT%{_datadir}/php/Smarty2
cp -a libs/* $RPM_BUILD_ROOT%{_datadir}/php/Smarty2/


%check
: Test autoloader and version
php -r '
require "%{buildroot}%{_datadir}/php/Smarty2/autoload.php";
$s = new Smarty();
printf("Smarty version \"%s\"\n", $s->_version);
version_compare($s->_version, "%{version}", "=") or exit(1);
'


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING.lib
%doc BUGS ChangeLog demo FAQ NEWS QUICK_START README
%doc RELEASE_NOTES TODO
%doc composer.json
%{_datadir}/php/Smarty2


%changelog
* Mon Aug  8 2016 Remi Collet <remi@remirepo.net> - 2.6.30-1
- update to 2.6.30
- sources from github
- add autoloader
- add minimal check for autoloader and version
- fix license installation

* Sun Dec 22 2013 Remi Collet <RPMS@FamilleCollet.com> - 2.6.28-1
- update to 2.6.28

* Sat Sep 29 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.6.27-1
- rename to php-Smarty2 and update to 2.6.27 for remi repo

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Oct 11 2009 Christopher Stone <chris.stone@gmail.com> 2.6.26-1
- Upstream sync
- Update %%source0 and %%URL

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 25 2009 Christopher Stone <chris.stone@gmail.com> 2.6.25-1
- Upstream sync

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 02 2008 Christopher Stone <chris.stone@gmail.com> 2.6.20-2
- Add security patch (bz #469648)
- Add RHL dist tag conditional for Requires

* Mon Oct 13 2008 Christopher Stone <chris.stone@gmail.com> 2.6.20-1
- Upstream sync

* Wed Feb 20 2008 Christopher Stone <chris.stone@gmail.com> 2.6.19-1
- Upstream sync
- Update %%license
- Fix file encoding

* Sun Apr 29 2007 Christopher Stone <chris.stone@gmail.com> 2.6.18-1
- Upstream sync

* Wed Feb 21 2007 Christopher Stone <chris.stone@gmail.com> 2.6.16-2
- Minor spec file changes/cleanups

* Fri Feb 09 2007 Orion Poplawski <orion@cora.nwra.com> 2.6.16-1
- Update to 2.6.16
- Install in /usr/share/php/Smarty
- Update php version requirement

* Tue May 16 2006 Orion Poplawski <orion@cora.nwra.com> 2.6.13-1
- Update to 2.6.13

* Tue Nov  1 2005 Orion Poplawski <orion@cora.nwra.com> 2.6.10-2
- Fix Source0 URL.

* Thu Oct 13 2005 Orion Poplawski <orion@cora.nwra.com> 2.6.10-1
- Initial Fedora Extras version
