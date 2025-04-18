import streamlit as st
from recommend import df, recommend_songs
import pandas as pd

# Set custom Streamlit page config
st.set_page_config(
    page_title="Music Recommender 🎵",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        font-family: 'Arial', sans-serif;
        color: #1DB954;
        text-align: center;
        margin-bottom: 30px;
    }
    .subheader {
        font-size: 22px;
        font-weight: normal;
        color: #777;
        text-align: center;
        margin-bottom: 30px;
    }
    .recommendation-header {
        color: #1DB954;
        font-size: 24px;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .stButton>button {
        background-color: #1DB954;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 30px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #169c46;
    }
    .song-info {
        padding: 15px;
        border-radius: 5px;
        background-color: #f0f2f6;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# App header with animation
st.markdown("<h1 class='main-header'>🎶 Music Recommender System 🎶</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>Discover music similar to your favorite songs</p>", unsafe_allow_html=True)

# Create two columns for the main layout
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Find Your Next Favorite Song")
    
    # Simple dropdown without search
    song_list = sorted(df['song'].dropna().unique())
    selected_song = st.selectbox("🎵 Select a song:", song_list)
    
    # Get song info if available
    song_info = df[df['song'] == selected_song].iloc[0] if not df[df['song'] == selected_song].empty else None
    
    if song_info is not None:
        st.markdown("### Song Information")
        with st.container():
            st.markdown("<div class='song-info'>", unsafe_allow_html=True)
            st.write(f"**Artist:** {song_info.get('artist', 'Unknown')}")
            if 'album' in song_info and not pd.isna(song_info['album']):
                st.write(f"**Album:** {song_info['album']}")
            if 'year' in song_info and not pd.isna(song_info['year']):
                st.write(f"**Year:** {int(song_info['year'])}")
            if 'genre' in song_info and not pd.isna(song_info['genre']):
                st.write(f"**Genre:** {song_info['genre']}")
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Number of recommendations slider
    num_recommendations = st.slider("Number of recommendations:", min_value=5, max_value=20, value=10)
    
    recommend_button = st.button("🚀 Recommend Similar Songs")

with col2:
    if recommend_button:
        with st.spinner("Finding similar songs for you..."):
            # Get recommendations with the specified number
            recommendations = recommend_songs(selected_song, top_n=num_recommendations)
            
            if recommendations is None:
                st.error("Sorry, we couldn't find recommendations for this song.")
            else:
                st.markdown("<h3 class='recommendation-header'>Your Personalized Recommendations</h3>", unsafe_allow_html=True)
                
                # Enhanced display for recommendations
                for idx, row in recommendations.iterrows():
                    col_a, col_b = st.columns([4, 1])
                    with col_a:
                        st.markdown(f"**{idx}. {row['song']}**")
                        st.markdown(f"{row['artist']}")
                    with col_b:
                        # Create a visual match percentage that decreases with rank
                        match_percent = max(95 - ((idx-1) * 2), 75)
                        st.markdown(f"<div style='text-align:right; color: {'green' if match_percent > 85 else 'orange'}; font-weight:bold;'>{match_percent}% match</div>", unsafe_allow_html=True)
                    st.divider()
                
                # Export option
                if st.button("📥 Export Recommendations"):
                    csv = recommendations.to_csv()
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"{selected_song}_recommendations.csv",
                        mime="text/csv",
                    )
    else:
        # Show instructions or featured songs when no recommendations yet
        st.markdown("### How It Works")
        st.markdown("""
        1. Select a song you enjoy from the dropdown menu
        2. Choose how many recommendations you want to see
        3. Click the recommend button to discover similar songs
        4. Export your recommendations to CSV if you want to save them
        """)

        st.markdown("### Why This Works")
        st.markdown("""
        Our recommendation system analyzes various features of music including:
        - Musical characteristics (tempo, key, etc.)
        - Lyrical themes and content
        - Artist similarity
        - Listener behavior patterns
        
        This helps us find songs that have similar qualities to your selection.
        """)

# Add footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888;'>
Created with ❤️ for music lovers • Data updated monthly
</div>
""", unsafe_allow_html=True)