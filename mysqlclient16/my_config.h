/*
 * Kluge to support multilib installation of both 32- and 64-bit RPMS:
 * we need to arrange that header files that appear in both RPMs are
 * identical.  Hence, this file is architecture-independent and calls
 * in an arch-dependent file that will appear in just one RPM.
 *
 * Note: this may well fail if user tries to use gcc's -I- option.
 * But that option is deprecated anyway.
 */
#if defined(__x86_64__)
#include "my_config_x86_64.h"
#elif defined(__ia64__)
#include "my_config_ia64.h"
#elif defined(__i386__)
#include "my_config_i386.h"
#elif defined(__ppc64__) || defined(__powerpc64__)
#include "my_config_ppc64.h"
#elif defined(__ppc__) || defined(__powerpc__)
#include "my_config_ppc.h"
#elif defined(__s390x__)
#include "my_config_s390x.h"
#elif defined(__s390__)
#include "my_config_s390.h"
#endif
