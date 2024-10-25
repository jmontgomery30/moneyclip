import os
import xml.etree.ElementTree as ET

def export_to_premiere(clips, output_path):
    root = ET.Element("xmeml", version="5")
    sequence = ET.SubElement(root, "sequence")
    media = ET.SubElement(sequence, "media")
    video = ET.SubElement(media, "video")
    track = ET.SubElement(video, "track")

    for i, clip in enumerate(clips):
        clip_item = ET.SubElement(track, "clipitem", id=f"clip_{i}")
        file = ET.SubElement(clip_item, "file", id=f"file_{i}")
        pathurl = ET.SubElement(file, "pathurl")
        pathurl.text = os.path.abspath(clip)

    tree = ET.ElementTree(root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    return f"Exported to Adobe Premiere Pro XML at {output_path}"

def export_to_davinci(clips, output_path):
    root = ET.Element("DaVinciResolveProject")
    media_pool = ET.SubElement(root, "MediaPool")
    timeline = ET.SubElement(media_pool, "Timeline")

    for i, clip in enumerate(clips):
        media_clip = ET.SubElement(timeline, "Clip", id=f"clip_{i}")
        file_path = ET.SubElement(media_clip, "FilePath")
        file_path.text = os.path.abspath(clip)

    tree = ET.ElementTree(root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    return f"Exported to DaVinci Resolve XML at {output_path}"

def custom_integration(clips, integration_type, output_path):
    if integration_type == "premiere":
        return export_to_premiere(clips, output_path)
    elif integration_type == "davinci":
        return export_to_davinci(clips, output_path)
    else:
        return "Unsupported integration type"
