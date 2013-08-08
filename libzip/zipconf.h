/*
 * Kluge to support multilib installation of both 32 and 64-bit RPMS:
 * we need to arrange that header files that appear in both RPMs are
 * identical.  Hence, this file is architecture-independent and calls
 * in an arch-dependent file that will appear in just one RPM.
 *
 * To avoid breaking arches not explicitly supported by Fedora, we
 * use this indirection file *only* on known multilib arches.
 * DO NOT INCLUDE THE NEW FILE DIRECTLY -- ALWAYS INCLUDE THIS ONE INSTEAD. */

#ifndef ZIPCONF_MULTILIB_H
#define ZIPCONF_MULTILIB_H

#include <bits/wordsize.h>
#if __WORDSIZE == 32
#include "zipconf-32.h"
#elif __WORDSIZE == 64
#include "zipconf-64.h"
#else
#error "unexpected value for __WORDSIZE macro"
#endif

#endif
