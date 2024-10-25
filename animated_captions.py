import cv2
import numpy as np
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def generate_captions(clip, captions, font='Arial', font_size=24, color='white', stroke_color='black', stroke_width=2):
    caption_clips = []
    for caption in captions:
        start, end, text = caption
        text_clip = TextClip(text, fontsize=font_size, font=font, color=color, stroke_color=stroke_color, stroke_width=stroke_width)
        text_clip = text_clip.set_position(('center', 'bottom')).set_start(start).set_duration(end - start)
        caption_clips.append(text_clip)
    
    final_clip = CompositeVideoClip([clip] + caption_clips)
    return final_clip

def customize_overlays(clip, overlays):
    overlay_clips = []
    for overlay in overlays:
        start, end, image_path, position = overlay
        overlay_clip = ImageClip(image_path).set_position(position).set_start(start).set_duration(end - start)
        overlay_clips.append(overlay_clip)
    
    final_clip = CompositeVideoClip([clip] + overlay_clips)
    return final_clip
