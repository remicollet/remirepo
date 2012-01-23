%define eclipse_base     %{_libdir}/eclipse
%define eclipse_dropin   %{_datadir}/eclipse/dropins

Name:      eclipse-phpeclipse
Version:   1.2.3
Release:   3%{?dist}
Summary:   PHP Eclipse plugin
Group:     Development/Tools
License:   CPL
URL:       http://phpeclipse.net/

Source0:   http://downloads.sourceforge.net/project/phpeclipse/a%29%20Eclipse%203.3.x/PHPEclipse-1.2.3/PHPEclipse-1.2.3.200910091456PRD-src.zip

# Fix broken PHP table of contents links in the Eclipse help
Patch0:    %{name}-broken-help-links.patch

# Don't package hidden eclipse project files
Patch1:    %{name}-fix-build-props.patch

# Integrate properly with Fedora's apache (probably does not want to go upstream)
Patch2:    %{name}-httpd-integration.patch

# Remove Windows specific preferences (probably does not want to go upstream)
Patch4:    %{name}-rm-win32-help.patch

# Fix a bug that passed the wrong file location to the external parser
Patch5:    %{name}-external-parser.patch

# Fix a bug that passed in the wrong URL to the browser
Patch6:    %{name}-external-preview.patch

# Fix an exception that was causing the phpmanual not to show when you first open the PHP perspective
Patch7:    %{name}-fix-phpmanual-view.patch

# Remove a reference that was causing a build failure on Eclipse 3.6+
Patch8:    %{name}-remove-internal-eclipse-ref.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch

BuildRequires:    java-devel
BuildRequires:    jpackage-utils
BuildRequires:    eclipse-pde >= 3.4
BuildRequires:    htmlparser
Requires:         java
Requires:         jpackage-utils
Requires:         eclipse-platform >= 3.4
Requires:         htmlparser
Requires:         php >= 5
Requires:         php-pecl-xdebug
Requires:         httpd

%description
PHPEclipse is an open source PHP IDE based on the Eclipse platform. Features
supported include syntax highlighting, content assist, PHP manual integration,
templates and support for the XDebug and DBG debuggers.

%prep
%setup -q -c

# apply patches
%patch0 -p0 -b .orig
%patch1 -p0 -b .orig
%patch2 -p0 -b .orig
%patch4 -p0 -b .orig
%patch5 -p0 -b .orig
%patch6 -p0 -b .orig
%patch7 -p0 -b .orig
%patch8 -p0 -b .orig

#remove bundled jars
find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

# ditch bundled libs in favor of building against fedora packaged libs
pushd plugins
build-jar-repository -s -p net.sourceforge.phpeclipse.phpmanual.htmlparser htmlparser
popd

# fix jar versions
find -name MANIFEST.MF | xargs sed --in-place "s/0.0.0/%{version}/"

%build
# build the main feature
%{eclipse_base}/buildscripts/pdebuild -f net.sourceforge.phpeclipse.feature

# build the debug features
%{eclipse_base}/buildscripts/pdebuild -f net.sourceforge.phpeclipse.debug.feature
%{eclipse_base}/buildscripts/pdebuild -f net.sourceforge.phpeclipse.xdebug.feature

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{eclipse_dropin}
unzip -q -d %{buildroot}%{eclipse_dropin}/phpeclipse        build/rpmBuild/net.sourceforge.phpeclipse.feature.zip
unzip -q -d %{buildroot}%{eclipse_dropin}/phpeclipse-debug  build/rpmBuild/net.sourceforge.phpeclipse.debug.feature.zip
unzip -q -d %{buildroot}%{eclipse_dropin}/phpeclipse-xdebug build/rpmBuild/net.sourceforge.phpeclipse.xdebug.feature.zip

# need to recreate the symlinks to libraries that were setup in "prep"
# because for some reason the ant copy task doesn't preserve them
pushd %{buildroot}%{eclipse_dropin}/phpeclipse/eclipse/plugins/net.sourceforge.phpeclipse.phpmanual.htmlparser_*
rm *.jar
build-jar-repository -s -p . htmlparser
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc features/net.sourceforge.phpeclipse.feature/cpl-v10.html
%{eclipse_dropin}/phpeclipse
%{eclipse_dropin}/phpeclipse-debug
%{eclipse_dropin}/phpeclipse-xdebug

%changelog
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Sep 25 2010 Mat Booth <fedora@matbooth.co.uk> 1.2.3-2
- Patch out a reference to an internal Eclipse class that was causing a build
  failure on Eclipse 3.6+

* Tue Jan 26 2010 Alexander Kurtakov <akurtako@redhat.com> 1.2.3-1
- Update to 1.2.3 release.
- Use upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 05 2009 Mat Booth <fedora@matbooth.co.uk> 1.2.1-4
- Drop GCJ AOT support.
- Add htmlparser dependency and drop htmlparser patch.
- Add patch to fix PartInitException and IllegalArgumentException in
  PHP Manual view.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 16 2008 Mat Booth <fedora@matbooth.co.uk> 1.2.1-2
- Add php-pecl-xdebug dependency.

* Fri Nov 14 2008 Mat Booth <fedora@matbooth.co.uk> 1.2.1-1
- Update to 1.2.1 and rebase patches.
- Fixes mark occurances bug in Eclipse 3.4 (#706).
- Fix NPE on shutdown if external tools are not used.

* Tue Sep 09 2008 Mat Booth <fedora@matbooth.co.uk> 1.2.0-0.4.svn1573
- Fix FTBFS due to patch fuzz.

* Wed Jul 30 2008 Andrew Overholt <overholt@redhat.com> 1.2.0-0.3.svn1573
- Update for building against Eclipse SDK 3.4.

* Sun Jun 29 2008 Mat Booth <fedora@matbooth.co.uk> 1.2.0-0.2.svn1573
- Add patch for Show External Preview functionality.
- Add patch for Use External PHP Parser functionality.

* Sat Jun 28 2008 Mat Booth <fedora@matbooth.co.uk> 1.2.0-0.1.svn1573
- New maintainer.
- Update to version 1.2.0 pre-release, svn1573.
- Adapt patches to new version.
- Update package for new Eclipse plugin guidelines.

* Mon Feb 11 2008 Brandon Holbrook <fedora at theholbrooks.org> 1.1.8-18
- Rebuild for gcc-4.3

* Sat Oct 20 2007 Brandon Holbrook <fedora at theholbrooks.org> 1.1.8-17
- Reference php5 instead of php4 in httpd.conf [bug 314831]

* Mon Dec 18 2006 Brandon Holbrook <fedora at theholbrooks.org> 1.1.8-16
- Require eclipse-pde-runtime

* Mon Dec 18 2006 Brandon Holbrook <fedora at theholbrooks.org> 1.1.8-15
- Own gcj/eclipse-phpeclipse/
- dos2unix cpl-v10.html

* Mon Dec 18 2006 Brandon Holbrook <fedora at theholbrooks.org> 1.1.8-13
- Replace datadir with libdir in sharedConfiguration to match new eclipse

* Tue Nov 28 2006 Brandon Holbrook <fedora at theholbrooks.org> 1.1.8-12
- Added -Dosgi.sharedConfiguration.area to build command

* Mon Nov 27 2006 Brandon Holbrook <fedora at theholbrooks.org> 1.1.8-11
- Removed maximum version Requirement for eclipse-platform

* Mon Nov 27 2006 Brandon Holbrook <fedora at theholbrooks.org> 1.1.8-10
- New java command to fix broken builds

* Thu Nov  2 2006 Brandon Holbrook <fedora at theholbrooks.org> 1.1.8-9
- Use included .html file as %%doc

* Tue Oct 31 2006 Brandon Holbrook <fedora at theholbrooks.org> 1.1.8-8
- New maintainer
- Fix Group, License, and Description
- Include a copy of the CPL-1.0

* Fri Aug 18 2006 Ben Konrath <bkonrath@redhat.com> 1.1.8-7
- Make external tools plugin re-locatable. 
- Enable GCJ support for Fedora.

* Fri Aug 18 2006 Ben Konrath <bkonrath@redhat.com> 1.1.8-6
- Use httpd.conf from external tools plugin instead of workspace to work around
  a race condition in the main phpeclipse plugin.

* Tue Aug 15 2006 Ben Konrath <bkonrath@redhat.com> 1.1.8-5
- Do not start httpd automatically in httpd integration patch.

* Fri Aug 11 2006 Ben Konrath <bkonrath@redhat.com> 1.1.8-4
- Add httpd integration patch.
- Move linux external tool preferences and httpd.conf to the httpd-integration
  patch.
- Remove README for httpd integration.
- Add patch to remove win32 help preferences.
- Add patch to compile against Eclipse SDK 3.2.

* Mon May 15 2006 Ben Konrath <bkonrath@redhat.com> 1.1.8-3
- Add preferences for the external tools on linux.
- Add README for httpd integration.

* Fri May 12 2006 Ben Konrath <bkonrath@redhat.com> 1.1.8-2
- Add requires.

* Wed Apr 26 2006 Ben Konrath <bkonrath@redhat.com> 1.1.8-1
- initial version
