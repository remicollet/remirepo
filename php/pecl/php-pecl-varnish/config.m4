 PHP_ARG_WITH(varnish, for varnish support,
 [  --with-varnish             Include varnish support])

if test "$PHP_VARNISH" != "no"; then

  AC_CHECK_HEADER(fcntl.h)
  AC_CHECK_HEADER(sys/types.h)
  AC_CHECK_HEADER(sys/socket.h)
  AC_CHECK_HEADER(netinet/in.h)
  AC_CHECK_HEADER(arpa/inet.h)
  AC_CHECK_HEADER(netdb.h)

  dnl # --with-varnish -> check with-path
  SEARCH_PATH="$PHP_VARNISH /usr/local /usr"
  SEARCH_FOR="varnishapi.h"
  AC_MSG_CHECKING([for varnish files in default path])
  for i in $SEARCH_PATH ; do
    if test -r $i/include/varnish/$SEARCH_FOR; then
      VARNISH_INCDIR=$i/include/varnish
      VARNISH_LIBDIR=$i/$PHP_LIBDIR
    elif test -r $i/include/$SEARCH_FOR; then
      VARNISH_INCDIR=$i/include
      VARNISH_LIBDIR=$i/$PHP_LIBDIR
    fi
  done
  
  if test -z "$VARNISH_INCDIR"; then
    AC_MSG_RESULT([not found])
    AC_MSG_ERROR([Please reinstall the varnish distribution])
  else
    AC_MSG_RESULT(headers found in $VARNISH_INCDIR)
  fi

  PHP_ADD_INCLUDE($VARNISH_INCDIR)
  AC_CHECK_HEADER([$VARNISH_INCDIR/varnishapi.h], [], AC_MSG_ERROR('varnishapi.h' header not found))
  AC_CHECK_HEADER([$VARNISH_INCDIR/vcli.h], [], AC_MSG_ERROR('vcli.h' header not found))
  AC_CHECK_HEADER([$VARNISH_INCDIR/vsl.h], [], AC_MSG_ERROR('vsl.h' header not found))

  LIBNAME=varnishapi
  LIBSYMBOL=VSM_New

  PHP_CHECK_LIBRARY($LIBNAME,$LIBSYMBOL,
  [
   PHP_ADD_LIBRARY_WITH_PATH($LIBNAME, $VARNISH_LIBDIR, VARNISH_SHARED_LIBADD)
   AC_DEFINE(HAVE_VARNISHAPILIB,1,[ ])
  ],[
    AC_MSG_ERROR([wrong varnishapi lib version or lib not found])
  ],[
    -L$VARNISH_LIBDIR -lm
  ])
 
  PHP_SUBST(VARNISH_SHARED_LIBADD)

  PHP_NEW_EXTENSION(varnish, varnish.c adm.c varnish_lib.c sha2.c exception.c stat.c log.c, $ext_shared)
fi
