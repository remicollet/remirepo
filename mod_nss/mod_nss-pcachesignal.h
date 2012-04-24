diff -u --recursive mod_nss-1.0.8.orig/nss_pcache.c mod_nss-1.0.8/nss_pcache.c
--- mod_nss-1.0.8.orig/nss_pcache.c	2008-07-02 10:54:06.000000000 -0400
+++ mod_nss-1.0.8/nss_pcache.c	2010-05-14 13:32:57.000000000 -0400
@@ -20,6 +20,7 @@
 #include <seccomon.h>
 #include <pk11func.h>
 #include <secmod.h>
+#include <signal.h>
 #include "nss_pcache.h"
 
 static char * getstr(const char * cmd, int el);
@@ -309,6 +310,8 @@
         exit(1);
     }
 
+    signal(SIGHUP, SIG_IGN);
+
     if (!strcasecmp(argv[1], "on"))
         fipsmode = 1;
 
Only in mod_nss-1.0.8: nss_pcache.c.rej
