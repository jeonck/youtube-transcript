import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_video_id(url):
    # 유튜브 URL에서 video ID를 추출하는 함수
    video_id_pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(video_id_pattern, url)
    return match.group(1) if match else None

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
        return transcript
    except Exception as e:
        return None

# 스트림릿 앱 UI
st.title('유튜브 자막 추출기')

# 사용자로부터 유튜브 URL 입력 받기
youtube_url = st.text_input('유튜브 영상 URL을 입력하세요:')

if youtube_url:
    video_id = extract_video_id(youtube_url)
    
    if video_id:
        transcript = get_transcript(video_id)
        
        if transcript:
            # 영상 미리보기 표시
            st.video(youtube_url)
            
            # 자막 텍스트 표시
            st.subheader('영상 자막:')
            full_text = ''
            for entry in transcript:
                full_text += f"{entry['text']}\n"
            
            st.text_area('전체 자막', full_text, height=300)
        else:
            st.error('이 영상에서 자막을 추출할 수 없습니다.')
    else:
        st.error('올바른 유튜브 URL을 입력해주세요.')
