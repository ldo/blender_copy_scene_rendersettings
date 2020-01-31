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
        "version" : (0, 4, 0),
        "blender" : (2, 81, 0),
        "location" : "Properties → Render → Copy From Scene",
        "description" :
            "copies render settings from another scene to this one.",
        "warning" : "",
        "wiki_url" : "",
        "tracker_url" : "",
        "category" : "Scene",
    }

def list_other_scenes(self, context) :
    "returns a list of enum items representing scenes in the current document" \
    " other than the active one."
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

    # render_props is the tree-structured table of scene settings to be copied.
    # Other dicts are subtrees that are referenced more than once.
    # Keys are attribute names; values are None for simple values to be
    # directly copied, or dicts denoting substructures to be recursively
    # processed.

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
    cycles_render_props = \
        { # Cycles-specific scene attributes
            "cycles" :
                { # CyclesRenderSettings fields
                    "aa_samples" : None,
                    "ao_bounces" : None,
                    "ao_bounces_render" : None,
                    "ao_samples" : None,
                    "bake_type" : None,
                    "blur_glossy" : None,
                    "camera_cull_margin" : None,
                    "caustics_reflective" : None,
                    "caustics_refractive" : None,
                    "debug_bvh_time_steps" : None,
                    "debug_bvh_type" : None,
                    "debug_cancel_timeout" : None,
                    "debug_opencl_device_type" : None,
                    "debug_opencl_kernel_single_program" : None,
                    "debug_opencl_kernel_type" : None,
                    "debug_opencl_mem_limit" : None,
                    "debug_reset_timeout" : None,
                    "debug_text_timeout" : None,
                    "debug_tile_size" : None,
                    "debug_use_cpu_avx" : None,
                    "debug_use_cpu_avx2" : None,
                    "debug_use_cpu_split_kernel" : None,
                    "debug_use_cpu_sse2" : None,
                    "debug_use_cpu_sse3" : None,
                    "debug_use_cpu_sse41" : None,
                    "debug_use_cuda_adaptive_compile" : None,
                    "debug_use_cuda_split_kernel" : None,
                    "debug_use_hair_bvh" : None,
                    "debug_use_opencl_debug" : None,
                    "debug_use_qbvh" : None,
                    "debug_use_spatial_splits" : None,
                    "device" : None,
                    "dicing_rate" : None,
                    "diffuse_bounces" : None,
                    "diffuse_samples" : None,
                    "distance_cull_margin" : None,
                    "feature_set" : None,
                    "film_exposure" : None,
                    "film_transparent" : None,
                    "filter_type" : None,
                    "filter_width" : None,
                    "glossy_bounces" : None,
                    "glossy_samples" : None,
                    "light_sampling_threshold" : None,
                    "max_bounces" : None,
                    "max_subdivisions" : None,
                    "mesh_light_samples" : None,
                    "motion_blur_position" : None,
                    "pixel_filter_type" : None,
                    "preview_aa_samples" : None,
                    "preview_active_layer" : None,
                    "preview_dicing_rate" : None,
                    # "preview_pause" : None, # skip this?
                    "preview_samples" : None,
                    "preview_start_resolution" : None,
                    "progressive" : None,
                    "rolling_shutter_duration" : None,
                    "rolling_shutter_type" : None,
                    "sample_all_lights_direct" : None,
                    "sample_all_lights_indirect" : None,
                    "sample_clamp_direct" : None,
                    "sample_clamp_indirect" : None,
                    "samples" : None,
                    "sampling_pattern" : None,
                    "seed" : None,
                    "shading_system" : None,
                    "subsurface_samples" : None,
                    "texture_limit" : None,
                    "texture_limit_render" : None,
                    "tile_order" : None,
                    "transmission_bounces" : None,
                    "transmission_samples" : None,
                    "transparent_max_bounces" : None,
                    "use_animated_seed" : None,
                    "use_camera_cull" : None,
                    "use_distance_cull" : None,
                    "use_layer_samples" : None,
                    "use_progressive_refine" : None,
                    "use_square_samples" : None,
                    "volume_bounces" : None,
                    "volume_max_steps" : None,
                    "volume_samples" : None,
                    "volume_step_size" : None,
                },
            "cycles_curves" :
                { # CyclesCurveRenderSettings fields
                    "cull_backfacing" : None,
                    "maximum_width" : None,
                    "minimum_width" : None,
                    "primitive" : None,
                    "resolution" : None,
                    "shape" : None,
                    "subdivisions" : None,
                    "use_curves" : None,
                },
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
            from_scene = bpy.data.scenes[from_scene_name]
            to_scene = context.scene
            copy_attrs \
              (
                root_name = "render",
                src = from_scene.render,
                dst = to_scene.render,
                attrs = self.render_props
              )
            if from_scene.render.engine == "CYCLES" and to_scene.render.engine == "CYCLES" :
                for props_name, props in self.cycles_render_props.items() :
                    copy_attrs \
                      (
                        root_name = props_name,
                        src = getattr(from_scene, props_name),
                        dst = getattr(to_scene, props_name),
                        attrs = props
                      )
                #end for
            #end if
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

    @classmethod
    def poll(celf, context) :
        return \
            context.space_data.context == "RENDER"
    #end poll

    def draw(self, context) :
        the_col = self.layout.column(align = True)
        the_col.prop(context.scene, "copy_render_scene", text = "From Scene")
        the_col.operator(CopySceneRenderAction.bl_idname, text = "Copy")
    #end draw

#end CopySceneRenderSettings


_classes_ = \
    (
        CopySceneRenderAction,
        CopySceneRenderSettings,
    )

def register() :
    bpy.types.Scene.copy_render_scene = bpy.props.EnumProperty \
      (
        items = list_other_scenes,
        name = "Scene",
        description = "Other scene from which to copy settings",
      )
    for ċlass in _classes_ :
        bpy.utils.register_class(ċlass)
    #end for
#end register

def unregister() :
    for ċlass in _classes_ :
        bpy.utils.unregister_class(ċlass)
    #end for
    if hasattr(bpy.types.Scene, "copy_render_scene") :
        delattr(bpy.types.Scene, "copy_render_scene")
    #end if
#end unregister

if __name__ == "__main__" :
    register()
#end if
