#!/bin/sh
# 
# This script is used to add and remove our extension from one of the Mozilla
# products directory, and is run from 'triggers' when the product is installed or
# upgraded, as well as when our package is installed. It is needed because
# Mozilla products are installed into versioned directories in /usr/lib[64]/<product>
# so we have to make a new symlink into the right directory when the
# application is installed or upgraded. But we would rather not leave
# our old symlinks behind, since that will cause the application
# directories not to be removed. (flash-player leaves its old symlinks behind,
# but that's no excuse for us to do the same...)
#
# Because I don't know any way of finding out what the new version
# is on installation or old version on uninstallation, we have
# to do things in a somewhat non-intuitive way
#
# The order on upgrade of the mozilla application is:
#
#  1. new package installed
#  2. triggerin for new package - we add all symlinks
#  3. triggerun for old package - we remove all symlinks
#  4. old package uninstalled
#  5. triggerpostun for old package - we add all symlinks
#
# Triggers are also run on self-upgrade, in that case we do:
#
#  1. new package installed
#  2. triggerin for new package - we add all symlinks
#  3. triggerun for old package - we remove all symlinks
#  4. old package uninstalled
#  5. postun for old package - we add all symlinks
#  6. triggerpostun for old package - NOT RUN (contrary to RPM docs)
#
#
# Script arguments:
# --appname: the mozilla application that this extension should register into.
#            Usually firefox or thunderbird.
# --extname: the name of the extension. It can be determined by looking at
#            the install.rdf file, in the extension directory. This file
#            contains several <em:id> tags. The extname parameter is the
#            content of the em:id tag which is not contained in the
#            em:targetApplication tag
# --extpath: the path where the extension will be installed
# --action:  either "install" or "remove"
# --basedir: the dirname of the directory where the target application is
#            installed. Usually /usr/lib or /usr/lib64>, it defaults to
#            /usr/lib
#
#
# Here's an example implementation in rpm scriptlets:
#
# %define tbupdate %{_libdir}/lightning/mozilla-extension-update.sh --appname thunderbird --extname {e2fda1a4-762b-4020-b5ad-a41df1933103} --basedir %{_libdir} --extpath %{_libdir}/lightning --action 
# 
# %post
# %{tbupdate} install || true
# 
# %preun
# # On removal (but not upgrade), remove the extention
# if [ $1 = 0 ] ; then
#     %{tbupdate} remove || true
# fi
# 
# %postun
# # This is needed not to reverse the effect of our preun, which
# # is guarded against upgrade, but because of our triggerun,
# # which is run on self-upgrade, though triggerpostun isn't
# if [ $1 != 0 ] ; then
#     %{tbupdate} install || true
# fi
# 
# %triggerin -- thunderbird
# %{tbupdate} install || true
# 
# %triggerun -- thunderbird
# %{tbupdate} remove || true
# 
# %triggerpostun -- thunderbird
# # Guard against being run post-self-uninstall, even though that
# # doesn't happen currently (see comment above)
# if [ "$1" != 0 ] ; then
#     %{tbupdate} install || true
# fi


die() {
	echo >&2 "$@"
	exit 0
}

usage() {
	die "Usage: $0 --appname <application-name> --extname <extension-name> --extpath <extension-path> --action <install|remove> [--basedir </usr/lib|/usr/lib64>]"
}

appname=
extname=
extpath=
action=
basedir=/usr/lib
while [ "$#" -gt "0" ]; do
	case "$1" in
	--appname)
		shift; appname="$1" ;;
	--extname)
		shift; extname="$1" ;;
	--extpath)
		shift; extpath="$1" ;;
	--action)
		shift; action="$1" ;;
	--basedir)
		shift; basedir="$1" ;;
	*) usage ;;
	esac
	shift
done


if [ "$action" = "install" ] ; then
	# Add symlinks to any mozilla directory that looks like it is part of a
	# currently installed package
	for d in $basedir/${appname}*; do
	    if [ "$d" = "$basedir/${appname}*" ] ; then
            continue
	    fi
	    link=$d/extensions/$extname
	    if [ -e $extpath -a -e $d/$appname-bin -a -d $d/extensions -a ! -L $link ] ; then
            ln -s $extpath $link
	    fi
	done
elif [ "$action" = "remove" ] ; then
	# Remove any symlinks we've created into any mozilla directory
	for d in $basedir/${appname}*; do
	    if [ "$d" = "$basedir/${appname}*" ] ; then
            continue
	    fi
	    link=$d/extensions/$extname
	    if [ -L $link ] ; then
            rm $link
	    fi
	done
else
    usage
fi

exit 0
