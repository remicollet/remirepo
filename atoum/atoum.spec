# remirepo spec file for atoum, from:
#
# Fedora spec file for atoum
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%global gh_commit    1d442459f3afd96375cf8b12f663c3e18253882d
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})

Name:           atoum
Version:        2.7.0
Release:        1%{?dist}
Summary:        PHP Unit Testing framework

Group:          Development/Libraries
License:        BSD
URL:            http://atoum.org
Source0:        https://github.com/%{name}/%{name}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:       php(language) >= 5.3.3
BuildRequires:       php-hash
BuildRequires:       php-json
BuildRequires:       php-session
BuildRequires:       php-tokenizer
BuildRequires:       php-xml

BuildRequires:       php-mbstring

BuildRequires:       php-cli
BuildRequires:       php-date
BuildRequires:       php-dom
BuildRequires:       php-pcre
BuildRequires:       php-phar
BuildRequires:       php-reflection
BuildRequires:       php-spl

# From composer.json, 	"require": {
#        "php": ">=5.3.3",
#        "ext-hash": "*",
#        "ext-json": "*",
#        "ext-session": "*",
#        "ext-tokenizer": "*",
#        "ext-xml": "*"
Requires:       php(language) >= 5.3.3
Requires:       php-hash
Requires:       php-json
Requires:       php-session
Requires:       php-tokenizer
Requires:       php-xml
# From composer.json, 	"suggest": {
#        "ext-mbstring": "Provides support for UTF-8 strings"
Requires:       php-mbstring
# From phpcompatinfo report for version 2.5.0
Requires:       php-cli
Requires:       php-date
Requires:       php-dom
Requires:       php-pcre
Requires:       php-phar
Requires:       php-reflection
Requires:       php-spl
%if 0%{?fedora} >= 21
Suggests:       php-pecl-xdebug
%endif

Provides: php-composer(atoum/atoum) = %{version}

%if %{?runselftest}%{!?runselftest:1}
%global with_tests   0%{!?_without_tests:1}
%else
%global with_tests   0%{?_with_tests:1}
%endif


%description
A simple, modern and intuitive unit testing framework for PHP!

It has been designed from the start with the following ideas in mind :
* Can be implemented rapidly ;
* Simplify test development ;
* Allow for writing reliable, readable, and clear unit tests ;

To accomplish that, it massively uses capabilities provided by PHP 5.3,
to give the developer a whole new way of writing unit tests.
Also, thanks to its fluid interface, it allows for writing unit tests in
a fashion close to natural language.
It also makes it easier to implement stubbing within tests, thanks to
intelligent uses of anonymous functions and closures.
atoum natively, and by default, performs the execution of each unit test
within a separate PHP process, to warrant isolation.
Of course, it can be used seamlessly for continuous integration, and given its
design, it can be made to cope with specific needs extremely easily.
atoum also accomplishes all of this without affecting performance, since it
has been developed to boast a reduced memory footprint while allowing for
hastened test execution.
It can also generate unit test execution reports in the Xunit format,
which makes it compatible with continuous integration tools such as Jenkins.
atoum also generates code coverage reports, in order to make it possible
to supervise unit tests.

Optional dependency:
- php-pecl-xdebug for code coverage reports


%prep
%setup -qn %{name}-%{gh_commit}

rm resources/configurations/.gitignore
rm scripts/git/.tag tests/units/classes/scripts/git/.tag
sed -i bin/%{name} \
    -e "s|__DIR__ . '/../|'%{_datadir}/%{name}/|"


%build
# Empty build section


%install
rm -rf %{buildroot}
# create needed directories
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_bindir}
install -m 0644 -p constants.php %{buildroot}%{_datadir}/%{name}
install -m 0755 bin/%{name} %{buildroot}%{_bindir}/%{name}
cp -pr classes   %{buildroot}%{_datadir}/%{name}
cp -pr resources %{buildroot}%{_datadir}/%{name}
cp -pr scripts   %{buildroot}%{_datadir}/%{name}
cp -pr tests     %{buildroot}%{_datadir}/%{name}


%check
%if %{with_tests}
cd tests/units
echo "date.timezone=UTC" >php.ini
export PHPRC=$(pwd)/php.ini

if which php70; then
    php70 runner.php --directories .
fi
if which php56; then
    php56 runner.php --directories .
else
    php runner.php --directories .
fi
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc ABOUT composer.json CREDITS.md FAQ.md README.md
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*


%changelog
* Sat May 21 2016 Remi Collet <remi@fedoraproject.org> - 2.7.0-1
- update to 2.7.0

* Fri Apr  8 2016 Remi Collet <remi@fedoraproject.org> - 2.6.1-1
- update to 2.6.1

* Wed Mar  9 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- update to 2.6.0

* Thu Jan 28 2016 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- update to 2.5.2

* Mon Jan 18 2016 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- update to 2.5.1

* Fri Jan  8 2016 Remi Collet <remi@fedoraproject.org> - 2.5.0-1
- update to 2.5.0

* Mon Dec  7 2015 Remi Collet <remi@fedoraproject.org> - 2.4.1-1
- update to 2.4.1

* Fri Oct 23 2015 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- update to 2.3.0
- drop patch merged upstream

* Thu Sep 17 2015 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- update to 2.2.2

* Thu Aug 27 2015 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- update to 2.2.1

* Sun Aug  2 2015 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- update to 2.2.0
- XDebug is optional

* Mon May 11 2015 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- update to 2.1.0
- update source0

* Tue Mar 24 2015 Remi Collet <RPMS@famillecollet.com> - 2.0.1-1
- add backport stuff

* Sun Mar 22 2015 Johan Cwiklinski <johan AT x-tnd DOT be> - 2.0.1-1
- Last upstream release

* Wed Jun 11 2014 Johan Cwiklinski <johan AT x-tnd DOT be> - 0-0.11.gite1f64c2
- Add provides for registered Packagist package

* Mon Jun 09 2014 Johan Cwiklinski <johan AT x-tnd DOT be> - 0-0.10.gite1f64c2
- Last upstream commit

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.9.git35a880e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 10 2014 Johan Cwiklinski <johan AT x-tnd DOT be> - 0.0.8.git35a880e
- Last upstream commit

* Sun Dec 08 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 0.0.7.gita68f365
- Last upstream commit

* Wed Aug 07 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 0.0.6.git587a130
- Last upstream commit

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.5.gita0452f6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 23 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 0.0.4.gita0452f6
- Last upstream commit

* Fri May 10 2013 Johan Cwiklinski <johan AT x-tnd DOt be> - 0.0.3.git3118d58
- Last upstream commit

* Sun Feb 10 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 0.0.2.gitdbfb82f
- Last upstream commit
- Rename package from php-atoum to atoum
- add missing requires
- change path to %%{_datadir}/%%{name}
- add tests and relevant BR

* Sun Jan 13 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 0-0.2.git724d3ee
- Use %%{real_name} instead of %%{name} in path

* Sun Jan 13 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 0-0.1.git724d3ee
- Initial Release
