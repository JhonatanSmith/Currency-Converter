#
# FreeType 2 Visual C++ on Win32
#


# Copyright (C) 1996-2022 by
# David Turner, Robert Wilhelm, and Werner Lemberg.
#
# This file is part of the FreeType project, and may only be used, modified,
# and distributed under the terms of the FreeType project license,
# LICENSE.TXT.  By continuing to use, modify, or distribute this file you
# indicate that you have read the license and understand and accept it
# fully.

# definitions of the export list
#
EXPORTS_LIST      = $(OBJ_DIR)/freetype.def
EXPORTS_OPTIONS   = /DEF:$(EXPORTS_LIST)
APINAMES_OPTIONS := -dfreetype.dll -w

include $(TOP_DIR)/builds/windows/win32-def.mk
include $(TOP_DIR)/builds/compiler/visualc.mk

# include linking instructions
include $(TOP_DIR)/builds/link_dos.mk


# EOF
