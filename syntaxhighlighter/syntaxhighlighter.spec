# spec file for syntaxhighlighter
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#

%global gh_owner   alexgorbatchev
%global gh_name    SyntaxHighlighter
%global gh_commit  682bf8cfd5a0686d51ed16325b72625ddf64ae11

Name:         syntaxhighlighter
Version:      3.0.83
Release:      2%{?dist}
Summary:      JavaScript syntax highlighter
Group:        Applications/Internet
# Dual licensed under the MIT and GPL licenses.
License:      MIT or GPLv2
URL:          http://alexgorbatchev.com/SyntaxHighlighter/

Source0:      https://github.com/%{gh_owner}/%{gh_name}/archive/%{gh_commit}/%{name}-%{version}-%{gh_commit}.tar.gz
Source1:      %{name}.conf
# Missing in github archive
Source2:      https://raw.github.com/%{gh_owner}/%{gh_name}/master/MIT-LICENSE
Source3:      https://raw.github.com/%{gh_owner}/%{gh_name}/master/GPL-LICENSE

# fix for recent PHP version
# not submitted, as upstream don't use phing anymore
Patch0:       %{name}-build.patch

BuildRoot:     %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:     noarch
BuildRequires: jre >= 1.6.0
BuildRequires: php-pear-phing


%description
SyntaxHighlighter is a fully functional self-contained code
syntax highlighter developed in JavaScript.


%package httpd
Summary:       Apache configuration for %{name}
Group:         Applications/Internet
Requires:      %{name} = %{version}-%{release}
Requires:      httpd

%description   httpd
This package provides the Apache configuration for
applications using an Alias to SyntaxHighlighter library.


%prep
%setup -q -n %{gh_name}-%{gh_commit}

: Create suitable examples, easy to run
sed -e 's:src="../scripts:src="/%{name}/scripts:' \
    -e 's:href="../styles:href="/%{name}/styles:' \
    -i demos/*php demos/*html

: Fix PHP syntax
%patch0 -p0 -b .old

: Fix revision
REV=%{version}
REV=${REV/*./}
sed -e s/@REVISION@/$REV/ \
    -i build/ext/RevisionTask.php

: License files
cp %{SOURCE2} %{SOURCE3} .


%build
cd build
phing -f build.xml

# phing don't correctly reports failure
[ -f output/scripts/shCore.js ] || exit 1


%install
rm -rf %{buildroot}

: install JavaScript
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -pr build/output/scripts %{buildroot}%{_datadir}/%{name}/scripts
cp -pr build/output/styles  %{buildroot}%{_datadir}/%{name}/styles

: install Apache configuration
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
install -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc GPL-LICENSE MIT-LICENSE demos
%{_datadir}/%{name}


%files httpd
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf


%changelog
* Sun Jun 16 2013 Remi Collet <remi@fedoraproject.org> - 3.0.83-2
- build from github sources

* Tue Jan 15 2013 Remi Collet <remi@fedoraproject.org> - 3.0.83-1
- initial package
