dnl config.m4 for extension xdiff
dnl adapted to use bundled copy of the library

PHP_ARG_WITH(xdiff, for xdiff support,
[  --with-xdiff             Include xdiff support])


if test "$PHP_XDIFF" != "no"; then

  dnl Checks for header files.
  AC_STDC_HEADERS
  AC_CHECK_HEADERS(stdio.h limits.h)

  dnl Checks for typedefs, structures, and compiler characteristics.
  AC_C_INLINE
  AC_C_VOLATILE
  AC_C_CONST
  AC_C_BIGENDIAN

  dnl Checks for library functions.
  AC_CHECK_FUNCS(memset memcmp memchr memcpy strlen malloc free realloc)

  LIBSRC="\
    libxdiff/xadler32.c \
    libxdiff/xalloc.c \
    libxdiff/xbdiff.c \
    libxdiff/xbpatchi.c \
    libxdiff/xdiffi.c \
    libxdiff/xemit.c \
    libxdiff/xmerge3.c \
    libxdiff/xmissing.c \
    libxdiff/xpatchi.c \
    libxdiff/xprepare.c \
    libxdiff/xrabdiff.c \
    libxdiff/xrabply.c \
    libxdiff/xutils.c \
    libxdiff/xversion.c \
  "

  PHP_NEW_EXTENSION(xdiff, xdiff.c $LIBSRC, $ext_shared)
  PHP_ADD_BUILD_DIR($ext_builddir/libxdiff, 1)
  PHP_ADD_INCLUDE([$ext_srcdir/libxdiff])
fi
