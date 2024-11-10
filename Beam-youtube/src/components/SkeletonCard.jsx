import React from 'react';

const SkeletonCard = () => {
  return (
    <div className="youtube-card-skeleton"  style={styles.card}>
      {/* Thumbnail Placeholder */}
      <div style={styles.thumbnail}></div>

      {/* Content Placeholder */}
      <div style={styles.content}>
        {/* Title Placeholder */}
        <div style={styles.title}></div>
        
        {/* Channel and Views Placeholder */}
        <div style={styles.subtitle}>
          <div style={styles.channelName}></div>
          <div style={styles.views}></div>
        </div>
      </div>
    </div>
  );
};

const styles = {
  card: {
    width: '320px',
    height: '280px',
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: '#f0f0f0',
    borderRadius: '8px',
    overflow: 'hidden',
    margin: '10px',
  },
  thumbnail: {
    width: '100%',
    height: '60%',
    backgroundColor: '#e0e0e0',
  },
  content: {
    padding: '10px',
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  title: {
    width: '90%',
    height: '16px',
    backgroundColor: '#d0d0d0',
    borderRadius: '4px',
  },
  subtitle: {
    display: 'flex',
    flexDirection: 'column',
    gap: '6px',
  },
  channelName: {
    width: '60%',
    height: '14px',
    backgroundColor: '#e0e0e0',
    borderRadius: '4px',
  },
  views: {
    width: '40%',
    height: '14px',
    backgroundColor: '#e0e0e0',
    borderRadius: '4px',
  },
};

export default SkeletonCard;
