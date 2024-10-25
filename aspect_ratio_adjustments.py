import cv2
import numpy as np
from moviepy.editor import VideoFileClip

def adjust_aspect_ratio(clip, target_aspect_ratio):
    width, height = clip.size
    current_aspect_ratio = width / height

    if current_aspect_ratio == target_aspect_ratio:
        return clip

    if target_aspect_ratio > current_aspect_ratio:
        new_width = int(height * target_aspect_ratio)
        new_height = height
    else:
        new_width = width
        new_height = int(width / target_aspect_ratio)

    resized_clip = clip.resize(newsize=(new_width, new_height))
    return resized_clip

def optimize_clips_for_platform(clips, platform):
    aspect_ratios = {
        'YouTube': 16/9,
        'Instagram': 1/1,
        'TikTok': 9/16
    }

    target_aspect_ratio = aspect_ratios.get(platform, 16/9)
    optimized_clips = [adjust_aspect_ratio(clip, target_aspect_ratio) for clip in clips]
    return optimized_clips
