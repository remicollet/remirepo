%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name phing
%global channel pear.phing.info

Summary:	A project build system based on Apache Ant
Name:		php-pear-phing
Version:	2.4.8
Release:	1%{?dist}

License:	LGPLv2
Group:		Development/Tools
Source0:	http://pear.phing.info/get/phing-%{version}.tgz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL:		http://phing.info/trac/

BuildArch:	noarch

BuildRequires:	php-pear
BuildRequires:	php-channel(pear.phing.info)
BuildRequires:	dos2unix
Requires:	php-cli >= 5.2.0
Requires:	php-pear >= 1.8.0
Requires:	php-pecl-xdebug >= 2.0.5
Requires:	php-channel(pear.phing.info)

Requires:	php-pear(pear.phpunit.de/PHPUnit) >= 3.6.0

Requires(post):	%{__pear}
Requires(postun): %{__pear}

Provides:	php-pear(%{channel}/%{pear_name}) = %{version}

%description
PHing Is Not GNU make; it's a project build system based on Apache Ant.

You can do anything with it that you could do with a traditional build
system like GNU make, and its use of simple XML build files and extensible
PHP "task" classes make it an easy-to-use and highly flexible build
framework. Features include file transformations (e.g. token replacement,
XSLT transformation, Smarty template transformations), file system operations,
interactive build support, SQL execution, CVS operations, tools for creating
PEAR packages, and much more.


%prep
%setup -qc
%{__mv} package.xml %{pear_name}-%{version}/%{pear_name}.xml
cd %{pear_name}-%{version}

%build
cd %{pear_name}-%{version}


%install
cd %{pear_name}-%{version}
%{__rm} -rf $RPM_BUILD_ROOT
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{pear_name}.xml

# not in the archive dos2unix $RPM_BUILD_ROOT/%{pear_docdir}/%{pear_name}/UPGRADE

%{__rm} -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

%{__mkdir_p} $RPM_BUILD_ROOT%{pear_xmldir}
%{__install} -pm 644 %{pear_name}.xml $RPM_BUILD_ROOT%{pear_xmldir}

%clean
%{__rm} -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
	%{pear_xmldir}/%{pear_name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
	%{__pear} uninstall --nodeps --ignore-errors --register-only \
		%{channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{_bindir}/phing
%doc %{pear_docdir}/%{pear_name}
%{pear_datadir}/%{pear_name}
%{pear_phpdir}/%{pear_name}
%{pear_phpdir}/%{pear_name}.php
%{pear_xmldir}/%{pear_name}.xml


%changelog
* Fri Nov 04 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.4.8-1
- upstream 2.4.8, rebuild for remi repository
- doc in /usr/share/doc/pear

* Thu Nov  3 2011 Christof Damian <christof@damian.net> - 2.4.8-1
- upstream 2.4.8

* Sat Jul 17 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.4.6-1
- rebuild for remi repository

* Fri Jul 15 2011 Christof Damian <christof@damian.net> - 2.4.6-1
- upstream 2.4.6

* Sat Mar  5 2011 Christof Damian <christof@damian.net> - 2.4.5-1
- remove requires hint

* Fri Mar  4 2011 Christof Damian <christof@damian.net> - 2.4.5-1
- upstream 2.4.5

* Sun Dec 12 2010 Remi Collet <RPMS@FamilleCollet.com> - 2.4.4-1
- rebuild for remi repository

* Wed Dec  8 2010 Christof Damian <christof@damian.net> - 2.4.4-1
- upstream 2.4.4

* Thu Nov 25 2010 Remi Collet <RPMS@FamilleCollet.com> - 2.4.3-1
- rebuild for remi repository

* Tue Nov 23 2010 Christof Damian <christof@damian.net> - 2.4.3-1
- upstream 2.4.3

* Fri Aug 05 2010 Remi Collet <RPMS@FamilleCollet.com> - 2.4.2-1
- rebuild for remi repository

* Sat Jul 31 2010 Christof Damian <christof@damian.net> - 2.4.2-1
- upstream 2.4.2

* Wed Jun 23 2010 Remi Collet <RPMS@FamilleCollet.com> - 2.4.1-1
- rebuild for remi repository

* Thu May 27 2010 Christof Damian <christof@damian.net> - 2.4.1-1
- upstream 2.4.1
- taking over package

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 19 2009 Remi Collet <RPMS@FamilleCollet.com> - 2.3.0-2
- rebuild for remi repository

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov  6 2007 Alexander Kahl <akahl@iconmobile.com> - 2.3.0-1
- stable version

* Tue Oct 30 2007 Alexander Kahl <akahl@iconmobile.com> - 2.3.0-0.1.RC2
- new release candidate version

* Tue Oct 16 2007 Alexander Kahl <akahl@iconmobile.com> - 2.3.0-0.1.RC1
- new release candidate version
- consequently adapted macros for all shell operations
- sanitized requires
- switched build root macro style
- additional s/\r\n/\n/g fixes

* Mon Sep  3 2007 Alexander Kahl <akahl@iconmobile.com> - 2.3.0-0.6.beta1
- name change (lowercase)
- changed pear datadir macro

* Fri Aug 24 2007 Alexander Kahl <akahl@iconmobile.com> - 2.3.0-0.5.beta1
- Fixed dos line terminators.

* Wed Aug 22 2007 Alexander Kahl <akahl@iconmobile.com> - 2.3.0-0.4.beta1
- New beta version.

* Tue Aug 21 2007 Alexander Kahl <akahl@iconmobile.com> - 2.2.0-3
- Adapted new Fedora layout.

* Tue Aug 21 2007 Alexander Kahl <akahl@iconmobile.com> - 2.2.0-2
- Updated PHPUnit dependency.

* Fri May 25 2007 Alexander Kahl <akahl@iconmobile.com> - 2.2.0-1
- Removed ant dependency.
- Added channel dependency.

* Wed May 23 2007 Alexander Kahl <akahl@iconmobile.com> 2.2.0-0
- Initial RPM release.
