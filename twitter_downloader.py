import streamlit as st
import yt_dlp

st.set_page_config(page_title="Twitter Video Downloader")
def get_video_formats(tweet_url):
    """Fetch available video formats for the given tweet URL."""
    ydl_opts = {"quiet": True, "no_warnings": True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(tweet_url, download=False)
            formats = info.get("formats", [])
            title = info.get("title", "twitter_video")
            return formats, title
    except Exception as e:
        st.error(f"Error fetching video info: {e}")
        return [], "twitter_video"

def filter_and_format_options(formats):
    """Filter video formats and create a list of readable options."""
    format_options = []
    format_ids = []
    for f in formats:
        if f.get("vcodec") != "none" and f.get("acodec") != "none":
            resolution = f.get("height", "Unknown")
            ext = f.get("ext", "mp4")
            size = f.get("filesize", "Unknown")
            if size != "Unknown" and size is not None:
                size = f"{size / (1024 * 1024):.2f} MB"
            else:
                size = "Size not available"
            format_id = f["format_id"]
            option = f"{resolution}p ({ext}) - {size}"
            format_options.append(option)
            format_ids.append(format_id)
    return format_options, format_ids
    
def download_twitter_video(tweet_url, format_id, output_path):
    """Download the video in the selected quality."""
    ydl_opts = {"outtmpl": output_path, "format": format_id}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([tweet_url])
        return True
    except Exception as e:
        st.error(f"Download failed: {e}")
        return False

def main():
    st.title("🐦Twitter Video Downloader")
    st.write("Enter a Twitter video URL and select the quality to download.")
    tweet_url = st.text_input("Twitter URL", "")
    if tweet_url:
        formats, video_title = get_video_formats(tweet_url)
        if formats:
            format_options, format_ids = filter_and_format_options(formats)
            if format_options:
                selected_option = st.selectbox("Select Video Quality", format_options)
                selected_format_id = format_ids[format_options.index(selected_option)]
                if st.button("Download"):
                    output_path = f"{video_title}.mp4"
                    with st.spinner("Downloading..."):
                        success = download_twitter_video(tweet_url, selected_format_id, output_path)
                        if success:
                            st.success(f"Video downloaded as '{output_path}'!")
                            with open(output_path, "rb") as file:
                                st.download_button(
                                    label="Click to download the file",
                                    data=file,
                                    file_name=output_path,
                                    mime="video/mp4"
                                )
            else:
                st.warning("No valid video formats found.")
        else:
            st.warning("Couldn’t retrieve video info. Check the URL.")

if __name__ == "__main__":
    main()
