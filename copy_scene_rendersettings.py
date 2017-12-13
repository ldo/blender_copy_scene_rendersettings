#+
# This Blender addon copies render settings from another scene in a
# document to the current one. There seems to be no way to share
# render settings datablocks between scenes, so this is the next best
# thing.
#-

import math
import sys # debug
import bpy

bl_info = \
    {
        "name" : "Copy Scene Render Settings",
        "author" : "Lawrence D'Oliveiro <ldo@geek-central.gen.nz>",
        "version" : (0, 2, 0),
        "blender" : (2, 7, 9),
        "location" : "Properties → Render → Copy From Scene",
        "description" :
            "copies render settings from another scene to this one.",
        "warning" : "",
        "wiki_url" : "",
        "tracker_url" : "",
        "category" : "Scene",
    }

def list_other_scenes(self, context) :
    result = tuple \
      (
        (s.name, s.name, "") for s in bpy.data.scenes if s.name != context.scene.name
      )
    if len(result) == 0 :
        result = (("", "<No other scenes>", ""),)
    #end if
    return \
        result
#end list_other_scenes

class CopySceneRenderAction(bpy.types.Operator) :
    bl_idname = "scene.copy_render_settings"
    bl_label = "Copy Scene Render Settings"

    image_format_settings_props = \
        { # ImageFormatSettings fields
            "cineon_black" : None,
            "cineon_gamma" : None,
            "cineon_white" : None,
            "color_depth" : None,
            "color_mode" : None,
            "compression" : None,
            "display_settings" :
                { # ColorManagedDisplaySettings fields
                    "display_device" : None,
                },
            "exr_codec" : None,
            "file_format" : None,
            "jpeg2k_codec" : None,
            "quality" : None,
            "stereo_3d_format" :
                { # Stereo3dFormat fields
                    "anaglyph_type" : None,
                    "display_mode" : None,
                    "interlace_type" : None,
                    "use_interlace_swap" : None,
                    "use_sidebyside_crosseyed" : None,
                    "use_squeezed_frame" : None,
                },
            "tiff_codec" : None,
            "use_cineon_log" : None,
            "use_jpeg2k_cinema_48" : None,
            "use_jpeg2k_cinema_preset" : None,
            "use_jpeg2k_ycc" : None,
            "use_preview" : None,
            "use_zbuffer" : None,
            "view_settings" :
                { # ColorManagedViewSettings fields
                    # "curve_mapping" readonly
                    "exposure" : None,
                    "gamma" : None,
                    "look" : None,
                    "use_curve_mapping" : None,
                    "view_transform" : None,
                },
            "views_format" : None,
        }
    scene_render_view_props = \
        { # SceneRenderView fields
            "camera_suffix" : None,
            "file_suffix" : None,
            "name" : None,
            "use" : None,
        }
    render_props = \
        { # RenderSettings fields
            "alpha_mode" : None,
            "antialiasing_samples" : None,
            "bake" :
                { # BakeSettings fields
                    "cage_extrusion" : None,
                    "cage_object" : None,
                    "filepath" : None,
                    "height" : None,
                    "image_settings" : image_format_settings_props,
                    "margin" : None,
                    "normal_b" : None,
                    "normal_g" : None,
                    "normal_r" : None,
                    "normal_space" : None,
                    # "pass_filter" readonly, contrary to docs!
                    "save_mode" : None,
                    "use_automatic_name" : None,
                    "use_cage" : None,
                    "use_clear" : None,
                    "use_pass_ambient_occlusion" : None,
                    "use_pass_color" : None,
                    "use_pass_diffuse" : None,
                    "use_pass_direct" : None,
                    "use_pass_emit" : None,
                    "use_pass_glossy" : None,
                    "use_pass_indirect" : None,
                    "use_pass_subsurface" : None,
                    "use_pass_transmission" : None,
                    "use_selected_to_active" : None,
                    "use_split_materials" : None,
                    "width" : None,
                },
            "bake_aa_mode" : None,
            "bake_bias" : None,
            "bake_distance" : None,
            "bake_margin" : None,
            "bake_normal_space" : None,
            "bake_quad_split" : None,
            "bake_samples" : None,
            "bake_type" : None,
            "bake_user_scale" : None,
            "border_max_x" : None,
            "border_max_y" : None,
            "border_min_x" : None,
            "border_min_y" : None,
            "display_mode" : None,
            "dither_intensity" : None,
            "edge_color" : None,
            "edge_threshold" : None,
            "engine" : None,
            "ffmpeg" :
                { # FFmpegSettings fields
                    "audio_bitrate" : None,
                    "audio_channels" : None,
                    "audio_codec" : None,
                    "audio_mixrate" : None,
                    "audio_volume" : None,
                    "buffersize" : None,
                    "codec" : None,
                    "constant_rate_factor" : None,
                    "ffmpeg_preset" : None,
                    "format" : None,
                    "gopsize" : None,
                    "max_b_frames" : None,
                    "maxrate" : None,
                    "minrate" : None,
                    "muxrate" : None,
                    "packetsize" : None,
                    "use_autosplit" : None,
                    "use_lossless_output" : None,
                    "use_max_b_frames" : None,
                    "video_bitrate" : None,
                },
            "field_order" : None,
            # "file_extension" readonly
            "filepath" : None,
            "filter_size" : None,
            "fps" : None,
            "fps_base" : None,
            "frame_map_new" : None,
            "frame_map_old" : None,
            # "has_multiple_engines" readonly
            "image_settings" : image_format_settings_props,
            # "is_movie_format" readonly
            # "layers" readonly
            "line_thickness" : None,
            "line_thickness_mode" : None,
            "motion_blur_samples" : None,
            "motion_blur_shutter" : None,
            # "motion_blur_shutter_curve"  readonly
            "octree_resolution" : None,
            "pixel_aspect_x" : None,
            "pixel_aspect_y" : None,
            "pixel_filter_type" : None,
            "preview_pixel_size" : None,
            "preview_start_resolution" : None,
            "raytrace_method" : None,
            "resolution_percentage" : None,
            "resolution_x" : None,
            "resolution_y" : None,
            "sequencer_gl_preview" : None,
            "simplify_ao_sss" : None,
            "simplify_child_particles" : None,
            "simplify_child_particles_render" : None,
            "simplify_shadow_samples" : None,
            "simplify_subdivision" : None,
            "simplify_subdivision_render" : None,
            "stamp_background" : None,
            "stamp_font_size" : None,
            "stamp_foreground" : None,
            "stamp_note_text" : None,
            "stereo_views" : scene_render_view_props,
                # collection of SceneRenderView
            "threads" : None,
            "threads_mode" : None,
            "tile_x" : None,
            "tile_y" : None,
            "use_antialiasing" : None,
            "use_bake_antialiasing" : None,
            "use_bake_clear" : None,
            "use_bake_lores_mesh" : None,
            "use_bake_multires" : None,
            "use_bake_normalize" : None,
            "use_bake_selected_to_active" : None,
            "use_bake_to_vertex_color" : None,
            "use_bake_user_scale" : None,
            "use_border" : None,
            "use_compositing" : None,
            "use_crop_to_border" : None,
            "use_edge_enhance" : None,
            "use_envmaps" : None,
            "use_fields" : None,
            "use_fields_still" : None,
            "use_file_extension" : None,
            "use_free_image_textures" : None,
            "use_freestyle" : None,
            "use_full_sample" : None,
            # "use_game_engine" readonly
            "use_instances" : None,
            "use_local_coords" : None,
            "use_lock_interface" : None,
            "use_motion_blur" : None,
            "use_multiview" : None,
            "use_overwrite" : None,
            "use_persistent_data" : None,
            "use_placeholder" : None,
            "use_raytrace" : None,
            "use_render_cache" : None,
            "use_save_buffers" : None,
            "use_sequencer" : None,
            "use_sequencer_gl_textured_solid" : None,
            # "use_shading_nodes" readonly
            "use_shadows" : None,
            "use_simplify" : None,
            "use_simplify_triangulate" : None,
            "use_single_layer" : None,
            # "use_spherical_stereo" readonly
            "use_sss" : None,
            "use_stamp" : None,
            "use_stamp_camera" : None,
            "use_stamp_date" : None,
            "use_stamp_filename" : None,
            "use_stamp_frame" : None,
            "use_stamp_labels" : None,
            "use_stamp_lens" : None,
            "use_stamp_marker" : None,
            "use_stamp_memory" : None,
            "use_stamp_note" : None,
            "use_stamp_render_time" : None,
            "use_stamp_scene" : None,
            "use_stamp_sequencer_strip" : None,
            "use_stamp_strip_meta" : None,
            "use_stamp_time" : None,
            "use_textures" : None,
            "use_world_space_shading" : None,
            "views" : scene_render_view_props,
                # collection of SceneRenderView
            "views_format" : None,
        }

    def execute(self, context) :

        def copy_attrs(root_name, src, dst, attrs) :
            is_collection = isinstance(src, bpy.types.bpy_prop_collection)
            assert is_collection == isinstance(dst, bpy.types.bpy_prop_collection)
            if is_collection :
                for i, (srcitem, dstitem) in enumerate(zip(src, dst)) :
                    copy_attrs("%s[%d]" % (root_name, i), srcitem, dstitem, attrs)
                #end for
            else :
                for name, val in attrs.items() :
                    full_name = root_name + "." + name
                    if hasattr(src, name) and hasattr(dst, name) :
                        if val != None :
                            copy_attrs(full_name, getattr(src, name), getattr(dst, name), val)
                        else :
                            setattr(dst, name, getattr(src, name))
                        #end if
                    elif hasattr(src, name) or hasattr(dst, name) :
                        sys.stderr.write \
                          (
                                "%s%s in src but%s in dst"
                            %
                                (
                                    full_name,
                                    (" not", "")[hasattr(src, name)],
                                    (" not", "")[hasattr(dst, name)],
                                )
                          ) # debug
                    #end if
                #end for
            #end if
        #end copy_attrs

    #begin execute
        from_scene_name = context.scene.copy_render_scene
        if from_scene_name != "" :
            copy_attrs \
              (
                root_name = "render",
                src = bpy.data.scenes[from_scene_name].render,
                dst = context.scene.render,
                attrs = self.render_props
              )
            status = {"FINISHED"}
        else :
            self.report({"ERROR"}, "No other scene")
            status = {"CANCELLED"}
        #end if
        return \
            status
    #end execute

#end CopySceneRenderAction

class CopySceneRenderSettings(bpy.types.Panel) :
    bl_idname = "RENDER_PT_copy_render_settings"
    bl_label = "Copy Render Settings"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW" # no default!

    def draw(self, context) :
        the_col = self.layout.column(align = True)
        the_col.prop(context.scene, "copy_render_scene", "From Scene")
        the_col.operator(CopySceneRenderAction.bl_idname, "Copy")
    #end draw

#end CopySceneRenderSettings

def register() :
    bpy.types.Scene.copy_render_scene = bpy.props.EnumProperty \
      (
        items = list_other_scenes,
        name = "Scene",
        description = "Other scene from which to copy settings",
      )
    bpy.utils.register_module(__name__)
#end register

def unregister() :
    bpy.utils.unregister_module(__name__)
    if hasattr(bpy.types.Scene, "copy_render_scene") :
        delattr(bpy.types.Scene, "copy_render_scene")
    #end if
#end unregister

if __name__ == "__main__" :
    register()
#end if
