Name:           dojo
Version:        1.6.1
Release:        1%{?dist}
Summary:        Modular JavaScript toolkit
Group:          Applications/Publishing
# See http://dojotoolkit.org/license
# and http://trac.dojotoolkit.org/browser/dojo/trunk/LICENSE
# The LICENSE files in the tarball are as follows: 
#   dojo/LICENSE: BSD or AFL2.1
#   dojo/_firebug/LICENSE: BSD
#   dojo/cldr/LICENSE: MIT
#   dojo/resources/LICENSE: BSD
#   dojox/LICENSE: BSD or AFL2.1
#   dojox/_sql/LICENSE: BSD
#   dojox/encoding/LICENSE: BSD
#   dojox/lang/LICENSE: MIT
#   dijit/LICENSE: BSD or AFL2.1
#   util/doh/LICENSE: BSD or AFL2.1
#   util/doh/_sounds/LICENSE: file has this text:
#   License Disclaimer:
#   
#   All contents of this directory are Copyright (c) the Dojo Foundation, with the
#   following exceptions:
#   -------------------------------------------------------------------------------
#   
#   woohoo.wav, doh.wav, dohaaa.wav:
#           * Copyright original authors.
#             Copied from:
#                   http://simpson-homer.com/homer-simpson-soundboard.html
#   
# However, that web site doesn't give provenance information or licensing info.
# For safety's sake, we don't ship these sound files in the built package
# (they appear to merely be "cute" sound effects for the test-running harness
# and thus unrelated to the primary function of the package)
License:        (BSD or AFL) and MIT and BSD
URL:            http://dojotoolkit.org/
Source0:        http://download.dojotoolkit.org/release-%{version}/dojo-release-%{version}.tar.gz
Source1:        %{name}.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       httpd

%description
Dojo is a JavaScript toolkit, providing cross-browser abstractions and widgets
for building dynamic web sites.

%prep
%setup -q -n %{name}-release-%{version}

# Delete sound files with unknown licensing from built package:
rm -rf %{_builddir}/%{name}-release-%{version}/util/doh/_sounds
rm -rf %{_builddir}/%{name}-release-%{version}/dojox/mobile/build
rm -rf %{_builddir}/%{name}-release-%{version}/dojox/storage/buildFlashStorage.sh
iconv -f iso8859-1 -t utf-8 dojo/cldr/LICENSE > dojo/cldr/LICENSE.conv && mv -f dojo/cldr/LICENSE.conv dojo/cldr/LICENSE

%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}

# Move licensing and documentation to docdir: 
pushd %{_builddir}/dojo-release-%{version}
  for f in `find . -name LICENSE -o -name README* -o -name NOTICES -o -name build.txt` ; do
    install -m 0444 -p -D $f $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}/$f
    rm $f
  done
popd

cp -pr ../dojo-release-%{version}/* $RPM_BUILD_ROOT%{_datadir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_datadir}/%{name}
%dir %{_docdir}/%{name}-%{version}
%dir %{_docdir}/%{name}-%{version}/%{name}
%dir %{_docdir}/%{name}-%{version}/dojox
%dir %{_docdir}/%{name}-%{version}/dijit
%doc %{_docdir}/%{name}-%{version}/*/*


%changelog
* Sat Jul 17 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.6.1-1
- rebuild for remi repository

* Sun Jun 26 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 1.6.1-1
- update to latest upstream

* Sun Mar 27 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 1.6.0-1
-update to latest upstream

* Tue Feb 01 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 1.5.0-1
- update to latest upstream

* Thu Jul 01 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 1.4.3-1
- update to latest upstream

* Mon Jul 21 2008 David Malcolm <dmalcolm@redhat.com> - 1.1.1-2
- fix removal of dojo/util/sounds
- fix mixed tabs/spaces in specfile

* Tue Jul 15 2008 David Malcolm <dmalcolm@redhat.com> - 1.1.1-1
- initial packaging

