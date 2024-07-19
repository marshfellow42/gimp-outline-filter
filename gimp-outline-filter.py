#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GIMP plugin to add an outline to a text layer

from gimpfu import *

def add_outline_to_text_layer(image, drawable, grow_by, outline_color):
    pdb.gimp_image_undo_group_start(image)
    
    # Ensure the selected layer is a text layer
    if pdb.gimp_item_is_text_layer(drawable):
        # Add the text layer to selection
        pdb.gimp_selection_layer_alpha(drawable)
        
        # Grow the selection
        pdb.gimp_selection_grow(image, grow_by)
        
        # Create a new layer to hold the outline
        outline_layer = pdb.gimp_layer_new(
            image, 
            pdb.gimp_image_width(image), 
            pdb.gimp_image_height(image), 
            RGBA_IMAGE, 
            "Outline Layer", 
            100, 
            NORMAL_MODE
        )
        
        # Insert the new layer above the original text layer
        text_layer_position = pdb.gimp_image_get_item_position(image, drawable)
        pdb.gimp_image_insert_layer(image, outline_layer, None, text_layer_position)
        
        # Move the new layer down by one position
        pdb.gimp_image_lower_item(image, outline_layer)

        # Set the foreground color to the chosen outline color
        pdb.gimp_context_set_foreground(outline_color)
        
        # Fill the selection with the foreground color
        pdb.gimp_edit_fill(outline_layer, FOREGROUND_FILL)
        
        # Remove selection
        pdb.gimp_selection_none(image)
    
    pdb.gimp_image_undo_group_end(image)
    
    # Refresh display
    pdb.gimp_displays_flush()

register(
    "python_fu_add_outline_to_text_layer",
    "Add an outline to a text layer",
    "Adds an outline to the currently selected text layer by growing the selection and filling it on a new layer.",
    "Anon",
    "Anon",
    "2024",
    "<Image>/Filters/Custom/Add Outline to Text Layer",
    "*",
    [
        (PF_INT, "grow_by", "Grow selection by (pixels)", 5),
        (PF_COLOR, "outline_color", "Outline Color", (255, 255, 255))
    ],
    [],
    add_outline_to_text_layer
)

main()
