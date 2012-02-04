/*
 * Kluge to support multilib installation of both 32 and 64-bit RPMS:
 * we need to arrange that header files that appear in both RPMs are
 * identical.  Hence, this file is architecture-independent and calls
 * in an arch-dependent file that will appear in just one RPM.
 *
 * To avoid breaking arches not explicitly supported by Fedora, we
 * use this indirection file *only* on known multilib arches.
 */
#if defined(__x86_64__)
#include "zipconf_x86_64.h"
#elif defined(__i386__)
#include "zipconf_i386.h"
#elif defined(__ppc64__) || defined(__powerpc64__)
#include "zipconf_ppc64.h"
#elif defined(__ppc__) || defined(__powerpc__)
#include "zipconf_ppc.h"
#elif defined(__s390x__)
#include "zipconf_s390x.h"
#elif defined(__s390__)
#include "zipconf_s390.h"
#elif defined(__sparc__) && defined(__arch64__)
#include "zipconf_sparc64.h"
#elif defined(__sparc__)
#include "zipconf_sparc.h"
#endif
