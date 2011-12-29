%define			php_extdir %(php-config --extension-dir || echo %{_libdir}/php)
%{!?php_version:%define php_version %(php-config --version || echo bad)}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# Private libraries are not be exposed globally by RPM
# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$


Name:		syck
Summary:	YAML for C, Python, and PHP

Version:	0.61
Release:	13%{?dist}

License:	BSD
Group:		System Environment/Libraries
URL:		http://whytheluckystiff.net/syck/

Source0:	http://pyyaml.org/download/pysyck/syck-%{version}+svn231+patches.tar.gz
Source1:	syck.ini

Patch0:		syck-0.55-libtool.patch
Patch1:		syck-nan.patch
# https://github.com/indeyets/syck/pull/7
Patch2:         syck-php54.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	gawk bison flex libtool
BuildRequires:	php-devel
BuildRequires:	python-devel
BuildRequires:	bison-devel
BuildRequires:	automake

%description
Syck is an extension for reading and writing YAML swiftly in popular scripting
languages. As Syck loads the YAML, it stores the data directly in your
language's symbol table. This means speed. This means power. This means Do not
disturb Syck because it is so focused on the task at hand that it will slay you
mortally if you get in its way. 

From http://yaml.org:
YAML(tm) (rhymes with "camel") is a straightforward machine parsable data
serialization format designed for human readability and interaction with
scripting languages such as Perl and Python. YAML is optimized for data
serialization, configuration settings, log files, Internet messaging and
filtering. 

%package	php
Summary:	YAML module for php
Group:		Development/Languages
%if %{?php_zend_api:1}0
Requires:	php(zend-abi) = %{php_zend_api}
Requires:	php(api) = %{php_core_api}
%else
Requires:	php = %{php_version}
%endif
Provides:	php-syck = %{version}-%{release}

%description	php
Syck is an extension for reading and writing YAML swiftly in popular scripting
languages. As Syck loads the YAML, it stores the data directly in your
language's symbol table. This means speed. This means power. This means Do not
disturb Syck because it is so focused on the task at hand that it will slay you
mortally if you get in its way. 

From http://yaml.org:
YAML(tm) (rhymes with "camel") is a straightforward machine parsable data
serialization format designed for human readability and interaction with
scripting languages such as Perl and Python. YAML is optimized for data
serialization, configuration settings, log files, Internet messaging and
filtering. 

The %{name}-php package contains the syck php extension.

%package	python
Summary:	YAML module for python
Group:		Development/Languages

%description	python
Syck is an extension for reading and writing YAML swiftly in popular scripting
languages. As Syck loads the YAML, it stores the data directly in your
language's symbol table. This means speed. This means power. This means Do not
disturb Syck because it is so focused on the task at hand that it will slay you
mortally if you get in its way. 

From http://yaml.org:
YAML(tm) (rhymes with "camel") is a straightforward machine parsable data
serialization format designed for human readability and interaction with
scripting languages such as Perl and Python. YAML is optimized for data
serialization, configuration settings, log files, Internet messaging and
filtering. 

The %{name}-python package contains the syck php extension.

%package	devel
Summary:	Static libraries and headers for developing with Syck
Group:		Development/Libraries
Requires:	syck = %{version}-%{release}
%description	devel
Syck is an extension for reading and writing YAML swiftly in popular scripting
languages. As Syck loads the YAML, it stores the data directly in your
language's symbol table. This means speed. This means power. This means Do not
disturb Syck because it is so focused on the task at hand that it will slay you
mortally if you get in its way. 

From http://yaml.org:
YAML(tm) (rhymes with "camel") is a straightforward machine parsable data
serialization format designed for human readability and interaction with
scripting languages such as Perl and Python. YAML is optimized for data
serialization, configuration settings, log files, Internet messaging and
filtering. 

This package contains the header files and static archive for developing with
Syck.

%prep
%setup -q -n syck-0.61+svn231+patches
%patch0 -p1 -b .libtool
%patch1 -p0 -b .nan
%patch2 -p1 -b .php54

%build
# Rebuild all
touch NEWS ChangeLog AUTHORS
autoreconf -f -i
%configure --disable-static

#%{__make} %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS"
#not parallel-build-safe
%{__make} CFLAGS="$RPM_OPT_FLAGS"

rm lib/*.la lib/.libs/*.la lib/.libs/*.lai
# Go into extensions directory
pushd ext

# PHP extension
pushd php
phpize
export php_cv_cc_rpath=no
CFLAGS="$RPM_OPT_FLAGS -I../../lib -L../../lib/.libs" %configure --with-syck=.
%{__make} %{?_smp_mflags}
popd # End php extension

# Python extension
pushd python
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
popd # End python extension

# Don't build the ruby extension, as syck is included since ruby 1.8.0.
# See the rubygarden: http://www.rubygarden.org/ruby?YamlInRuby

# Get out of extension
popd

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# Go into extensions directory
pushd ext

# PHP extension
pushd php
%{__make} install INSTALL_ROOT=$RPM_BUILD_ROOT
popd # End php extension

install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/syck.ini

# Python extension
pushd python
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd # End python extension

# Get out of extension
popd

%check
# minimal load test for the PHP extension
LD_LIBRARY_PATH=%{buildroot}%{_libdir} php -n \
    -d extension_dir=%{buildroot}%{php_extdir} \
    -d extension=syck.so -m \
    | grep syck


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,0755)
%doc COPYING README TODO RELEASE CHANGELOG
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,0755)
%doc README.EXT README.BYTECODE
%{_libdir}/*.so
%{_includedir}/*.h

%files python
%defattr(-,root,root,0755)
%{python_sitearch}/*

%files php
%defattr(-,root,root,0755)
%{php_extdir}/*.so
%config(noreplace) %{_sysconfdir}/php.d/syck.ini

%changelog
* Thu Dec 29 2011 Remi Collet <remi@fedoraproject.org> - 0.61-13
- build with php 5.4, with patch
- add minimal load test for PHP extension
- add provides filters

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.61-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.61-12
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Feb 12 2010 Oliver Falk <oliver@linux-kernel.at> - 0.61-11
- Force autotools rebuild

* Fri Feb 12 2010 Oliver Falk <oliver@linux-kernel.at> - 0.61-10
- NO update to 0.70 for now - it's somewhat b0rken
- Disable building of static libs #556095

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.61-9.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Remi Collet <Fedora@FamilleCollet.com> - 0.61-8.3
- rebuild for new PHP 5.3.0 ABI (20090626)
- add syck-nan.patch

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.61-8.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 07 2009 Caolán McNamara <caolanm@redhat.com> - 0.61-7.2
- build isn't parallel-make safe

* Fri Dec 19 2008 Oliver Falk <oliver@linux-kernel.at>	- 0.61-7.1
- Add bison-devel as BR

* Fri Dec 19 2008 Oliver Falk <oliver@linux-kernel.at>	- 0.61-7
- Rebuild for deps

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.61-6.1
- Rebuild for Python 2.6

* Fri Jun 06 2008 Oliver Falk <oliver@linux-kernel.at>	- 0.61-5.1
- Add syck.ini to files

* Fri Jun 06 2008 Oliver Falk <oliver@linux-kernel.at>	- 0.61-5
- Rebuild to fix bug #447561
- Add syck.ini

* Tue Feb 19 2008 Oliver Falk <oliver@linux-kernel.at>	- 0.61-4.3
- Yet another python fix

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.61-4.2
- Autorebuild for GCC 4.3

* Mon Feb 18 2008 Oliver Falk <oliver@linux-kernel.at>	- 0.61-3.2
* Make egginfo work and clean up python stuff in spec

* Sat Feb 16 2008 Oliver Falk <oliver@linux-kernel.at>	- 0.61-3.1
- Rebuild against new PHP

* Thu Sep 20 2007 Oliver Falk <oliver@linux-kernel.at>	- 0.61-2
- Rebuild against new PHP

* Tue Aug 21 2007 Oliver Falk <oliver@linux-kernel.at>	- 0.61-1
- Update
- Clean up spec a bit
- Rebuild to make Jesse happy

* Thu Jul 19 2007 Jesse Keating <jkeating@redhat.com> - 0.55-17
- Rebuild against new PHP, again.

* Thu May 24 2007 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.55-16
- Rebuild against new PHP

* Wed Mar 14 2007 Oliver Falk <oliver@linux-kernel.at>     - 0.55-15
- Bug #205438, don't ghost pyo any longer

* Mon Feb 26 2007 Oliver Falk <oliver@linux-kernel.at>     - 0.55-14
- Rebuild against new PHP

* Sun Dec 24 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.55-13
- Rebuild with Python 2.5.

* Fri Dec 01 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.55-12
- Adapt to new autoconf in rawhide.

* Thu Nov 30 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.55-11
- Rebuild for updated php.

* Fri Sep 01 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.55-10
- Rebuild.

* Sat Aug 26 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.55-9
- Add BR: libtool to work with the minimal buildroot.

* Sat Aug 26 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.55-8
- Rebuild.

* Wed Feb 22 2006 Oliver Falk <oliver@linux-kernel.at>		- 0.55-7
- Bug #175619

* Fri Sep 16 2005 Oliver Falk <oliver@linux-kernel.at>		- 0.55-6
- Compile against PHP 5.0.5

* Thu Aug 25 2005 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.55-5
- Stop using a dynamically generated php-version in the BR.
- Create a devel package
- Correct libtool patch and implementation
- Implement some ugly workarounds to get the php module to build correctly
- Change Groups to be more like Core packages
- Enhance Summaries and description
- %%ghost the *.pyos.

* Thu Aug 25 2005 Oliver Falk <oliver@linux-kernel.at>		- 0.55-4
- Bugs from #165686
- Add dist-tag

* Wed Aug 24 2005 Oliver Falk <oliver@linux-kernel.at>		- 0.55-3
- Fix filelist
- Fix php module path - dynamic

* Wed Aug 24 2005 Oliver Falk <oliver@linux-kernel.at>		- 0.55-2
- Bug #165686

* Thu May 19 2005 Oliver Falk <oliver@linux-kernel.at>		- 0.55-1
- Update
- Remove patch, as it works without now

* Fri Apr 08 2005 Oliver Falk <oliver@linux-kernel.at>		- 0.54-2
- Patch gram.y (taken from CVS) to fix compilation on Fedora Core 3
  (Should fix compilation...)

* Tue Apr 05 2005 Oliver Falk <oliver@linux-kernel.at>		- 0.53-1.1
- Force rebuild on buildsys

* Sun Apr 03 2005 Oliver Falk <oliver@linux-kernel.at>		- 0.53-1
- Update

* Fri Mar 25 2005 Oliver Falk <oliver@linux-kernel.at>		- 0.51-1.2
- Force rebuild at automated build system...

* Fri Mar 25 2005 Oliver Falk <oliver@linux-kernel.at>		- 0.51-1.1
- Rebuild
- Specfile cleanup

* Tue Mar 15 2005 Oliver Falk <oliver@linux-kernel.at>		- 0.51-1
- Update
- Delete python and php comments
- Move syck package to my cvs server

* Wed Sep 22 2004 Oliver Falk <oliver@linux-kernel.at>		- 0.45-1
- Initial build
