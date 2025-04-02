from mutagen import File as MutagenFile
from pymediainfo import MediaInfo
def extractVideoMetadata(filepath):
    media_info = MediaInfo.parse(filepath)
    metadata = {
        "title": None,
        "show": None,
        "season": None,
        "episode": None,
        "episode_id": None,
        "release_date": None,
        "album_artist": None,
        "genre": None,
        "year": None,
        "description": None,
        "long_description": None,
        "rating": None,
        "runtime": None,
        "cover_exists": False,
    }

    for track in media_info.tracks:
        if track.track_type == "General":
            metadata["title"] = track.title
            metadata["show"] = track.collection
            metadata["season"] = track.season
            metadata["episode"] = track.part
            metadata["episode_id"] = track.part_id
            metadata["release_date"] = track.recorded_date
            metadata["album_artist"] = track.album_performer
            metadata["genre"] = track.genre
            metadata["year"] = track.recorded_date[:4] if track.recorded_date else None
            metadata["description"] = track.description
            metadata["long_description"] = getattr(track, "long_description", None)
            metadata["rating"] = getattr(track, "content_rating", None)
            metadata["runtime"] = track.duration / 60000 if track.duration else None

        elif track.track_type == "Image":
            metadata["cover_exists"] = True

    return metadata


def extract_metadata(filepath):
    audio = MutagenFile(filepath)
    if not audio or not audio.info:
        return None

    def get_tag(*keys):
        for key in keys:
            if key in audio:
                value = audio[key]
                if isinstance(value, list):
                    return value[0]
                elif hasattr(value, 'text'):
                    return value.text[0]
                return str(value)
        return None
    title = get_tag("TIT2", "title")
    artist = get_tag("TPE1", "artist")
    album = get_tag("TALB", "album")
    duration = audio.info.length
    return {
        "title": title,
        "artist": artist,
        "album": album,
        "duration": duration,
    }
