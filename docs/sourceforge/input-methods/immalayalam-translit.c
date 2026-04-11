/* GTK - The GIMP Toolkit
 * Copyright (C) 2000 Red Hat Software
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Library General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Library General Public License for more details.
 *
 * You should have received a copy of the GNU Library General Public
 * License along with this library; if not, write to the
 * Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 *
 * Author: Owen Taylor <otaylor@redhat.com>
 *
 */

#include <string.h>

#include <gdk/gdkkeysyms.h>

#include "gtk/gtkintl.h"
#include "gtk/gtkimcontextsimple.h"
#include "gtk/gtkimmodule.h"

GType type_malayalam_translit = 0;

static void malayalam_translit_class_init (GtkIMContextSimpleClass *class);
static void malayalam_translit_init (GtkIMContextSimple *im_context);

static void
malayalam_translit_register_type (GTypeModule *module)
{
  static const GTypeInfo object_info   {
    sizeof (GtkIMContextSimpleClass),
    (GBaseInitFunc) NULL,
    (GBaseFinalizeFunc) NULL,
    (GClassInitFunc) malayalam_translit_class_init,
    NULL,           /* class_finalize */
    NULL,           /* class_data */
    sizeof (GtkIMContextSimple),
    0,
    (GtkObjectInitFunc) malayalam_translit_init,
  };

  type_malayalam_translit = 
    g_type_module_register_type (module,
				 GTK_TYPE_IM_CONTEXT_SIMPLE,
				 "GtkIMContextMalayalamTranslit",
				 &object_info, 0);
}

/* The sequences here match the sequences used in the emacs quail
 * mode cryllic-translit; they allow entering all characters
 * in iso-8859-5
 */
static guint16 malayalam_compose_seqs[] = {
  GDK_plus,     0,  	0,      0,      0,      0x0D4D, 
  GDK_plus,     GDK_period,  	GDK_r,      0,      0,      0x0D43, 
  GDK_plus,     GDK_A,  0,      0,      0,      0x0D3e, 
  GDK_plus,     GDK_E,  0,      0,      0,      0x0D47, 
  GDK_plus,     GDK_I,  0,      0,      0,      0x0D40, 
  GDK_plus,     GDK_O,  0,      0,      0,      0x0D4b, 
  GDK_plus,     GDK_U,  0,      0,      0,      0x0D42, 
  GDK_plus,     GDK_a,  GDK_a,  0,      0,      0x0D3e, 
  GDK_plus,     GDK_a,  GDK_i,  0,      0,      0x0D48, 
  GDK_plus,     GDK_a,  GDK_u,  0,      0,      0x0D4c, 
  GDK_plus,     GDK_e,  0,      0,      0,      0x0D46, 
  GDK_plus,     GDK_e,  GDK_e,      0,      0,      0x0D47, 
  GDK_plus,     GDK_i,  0,      0,      0,      0x0D3f, 
  GDK_plus,     GDK_i,  GDK_i,  0,      0,      0x0D40, 
  GDK_plus,     GDK_o,  0,      0,      0,      0x0D4a, 
  GDK_plus,     GDK_o,  GDK_o,  0,      0,      0x0D4b, 
  GDK_plus,     GDK_u,  0,      0,      0,      0x0D41, 
  GDK_plus,     GDK_u,  GDK_u,  0,      0,      0x0D42, 
  GDK_period,   GDK_r,  0,      0,      0,      0x0d0b, 
  GDK_0,   	0,  	0,      0,      0,      0x0d66, 
  GDK_1,   	0,  	0,      0,      0,      0x0d67, 
  GDK_2,   	0,  	0,      0,      0,      0x0d68, 
  GDK_3,   	0,  	0,      0,      0,      0x0d69, 
  GDK_4,   	0,  	0,      0,      0,      0x0d6a, 
  GDK_5,   	0,  	0,      0,      0,      0x0d6b, 
  GDK_6,   	0,  	0,      0,      0,      0x0d6c, 
  GDK_7,   	0,  	0,      0,      0,      0x0d6d, 
  GDK_8,   	0,  	0,      0,      0,      0x0d6e, 
  GDK_9,   	0,  	0,      0,      0,      0x0d6f, 
  GDK_A,	0,	0,	0,	0,	0x0d05,	
  GDK_D,	GDK_a,	0,	0,	0,	0x0d21,	
  GDK_D,	GDK_h,	GDK_a,	0,	0,	0x0d22,	
  GDK_E,	0,	0,	0,	0,	0x0d0F,	
  GDK_H,	0,	0,	0,	0,	0x0d03,	
  GDK_I,	0,	0,	0,	0,	0x0d08,	
  GDK_L,	GDK_a,	0,	0,	0,	0x0d33,	
  GDK_M,	0,	0,	0,	0,	0x0d02,	
  GDK_N,	GDK_a,	0,	0,	0,	0x0d23,	
  GDK_O,	0,	0,	0,	0,	0x0d13,	
  GDK_R,	GDK_a,	0,	0,	0,	0x0d31,	
  GDK_T,	GDK_a,	0,	0,	0,	0x0d1F,	
  GDK_T,	GDK_h,  GDK_a,	0,	0,	0x0d20,	
  GDK_U,	0,	0,	0,	0,	0x0d0A,	
  GDK_Z,	0,	0,	0,	0,	0x200d,	
  GDK_a,	0,	0,	0,	0,	0x0d05,	
  GDK_a,	GDK_a,	0,	0,	0,	0x0d06,	
  GDK_a,	GDK_i,	0,	0,	0,	0x0d10,	
  GDK_a,	GDK_u,	0,	0,	0,	0x0d14,	
  GDK_b,	GDK_a,	0,	0,	0,	0x0d2c,	
  GDK_b,	GDK_h,	GDK_a,	0,	0,	0x0d2d,	
  GDK_c,	GDK_a,	0,	0,	0,	0x0d1A,	
  GDK_c,	GDK_h,	GDK_a,	0,	0,	0x0d1B,	
  GDK_d,	GDK_a,	0,	0,	0,	0x0d26,	
  GDK_d,	GDK_h,	GDK_a,	0,	0,	0x0d27,	
  GDK_e,	0,	0,	0,	0,	0x0d0e,	
  GDK_e,	GDK_e,	0,	0,	0,	0x0d0f,	
  GDK_f,	GDK_a,	0,	0,	0,	0x0d2b,	
  GDK_g,	GDK_a,	0,	0,	0,	0x0d17,	
  GDK_g,	GDK_h,	GDK_a,	0,	0,	0x0d18,	
  GDK_h,	GDK_a,	0,	0,	0,	0x0d39,	
  GDK_i,	0,	0,	0,	0,	0x0d07,	
  GDK_i,	GDK_i,	0,	0,	0,	0x0d08,	
  GDK_j,	GDK_a,	0,	0,	0,	0x0d1c,	
  GDK_j,	GDK_h,	GDK_a,	0,	0,	0x0d1d,	
  GDK_k,	GDK_a,	0,	0,	0,	0x0d15,	
  GDK_k,	GDK_h,	GDK_a,	0,	0,	0x0d16,	
  GDK_l,	GDK_a,	0,	0,	0,	0x0d32,	
  GDK_m,	GDK_a,	0,	0,	0,	0x0d2e,	

  GDK_n,	GDK_quotedbl,	0,	0,	0,	0x0d19,	
  GDK_n,	GDK_a,	0,	0,	0,	0x0d28,	
  GDK_n,	GDK_asciitilde,	0,	0,	0,	0x0d1e,	
  GDK_o,	0,	0,	0,	0,	0x0d12,	
  GDK_o,	GDK_o,	0,	0,	0,	0x0d13,	
  GDK_p,	GDK_a,	0,	0,	0,	0x0d2a,	
  GDK_p,	GDK_h,	GDK_a,	0,	0,	0x0d2b,	
  GDK_r,	GDK_a,	0,	0,	0,	0x0d30,	
  GDK_s,	GDK_a,	0,	0,	0,	0x0d38,	
  GDK_s,	GDK_h,	GDK_a,	0,	0,	0x0d36,	
  GDK_t,	GDK_underscore,	GDK_a,	0,	0,	0x0d31,	
  GDK_t,	GDK_a,	0,	0,	0,	0x0d24,	
  GDK_t,	GDK_h,	GDK_a,	0,	0,	0x0d25,	
  GDK_u,	0,	0,	0,	0,	0x0d09,	
  GDK_u,	GDK_u,	0,	0,	0,	0x0d0a,	
  GDK_v,	GDK_a,	0,	0,	0,	0x0d35,	
  GDK_y,	GDK_a,	0,	0,	0,	0x0d2f,	
  GDK_z,	GDK_h,	GDK_a,	0,	0,	0x0d34,	
};

static void
malayalam_translit_class_init (GtkIMContextSimpleClass *class)
{
}

static void
malayalam_translit_init (GtkIMContextSimple *im_context)
{
  gtk_im_context_simple_add_table (im_context,
				   malayalam_compose_seqs,
				   4,
				   G_N_ELEMENTS (malayalam_compose_seqs) / (4 + 2));
}

static const GtkIMContextInfo malayalam_translit_info = { 
  "malayalam_translit",		   /* ID */
  N_("Malayalam (Transliterated)"), /* Human readable name */
  "gtk+",			   /* Translation domain */
   GTK_LOCALEDIR,		   /* Dir for bindtextdomain (not strictly needed for "gtk+") */
  ""			           /* Languages for which this module is the default */
};

static const GtkIMContextInfo *info_list[] = {
  &malayalam_translit_info
};

void
im_module_init (GTypeModule *module)
{
  malayalam_translit_register_type (module);
}

void 
im_module_exit (void)
{
}

void 
im_module_list (const GtkIMContextInfo ***contexts,
		int                      *n_contexts)
{
  *contexts = info_list;
  *n_contexts = G_N_ELEMENTS (info_list);
}

GtkIMContext *
im_module_create (const gchar *context_id)
{
  if (strcmp (context_id, "malayalam_translit") == 0)
    return GTK_IM_CONTEXT (g_object_new (type_malayalam_translit, NULL));
  else
    return NULL;
}
