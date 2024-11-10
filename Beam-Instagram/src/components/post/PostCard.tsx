import React from 'react';
import { View, Text, Image, StyleSheet, ImageBackground, ScrollView } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

const InstagramPostCard = ({ post,isThirdImageCentered }) => {
  // console.log(post);
  return (
    <ScrollView contentContainerStyle={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Image
          source={{ uri: post["user"]["image_url"] }} // Replace with actual profile image URL
          style={styles.profileImage}
        />
        <View style={styles.headerTextContainer}>
          <Text style={styles.username}>{post["user"]["username"]}</Text>
          <Text style={styles.followers}>Followers 1000</Text>
        </View>
        <Ionicons name="checkmark-circle" size={18} color="blue" style={styles.verifiedIcon} />
        <Ionicons name="ellipsis-horizontal" size={24} color="black" style={styles.moreIcon} />
      </View>

      {/* Post Image */}
      <ImageBackground
        source={{ uri: post['image_url'] }} // Replace with actual post image URL
        style={styles.postImage}
      >
        {/* Image Contents */}
        {/* <View style={post["id"]==3?styles.imageOverlay2:styles.imageOverlay}> */}
        <View style={isThirdImageCentered &&(post["id"]==3 || post["id"]==5 )? styles.imageOverlay2 : styles.imageOverlay} />
        {/* </View> */}
      </ImageBackground>

      {/* Post Content */}
      <View style={styles.content}>
        <Text style={styles.caption}>
          Advent of cyber 2022 <Text style={styles.hashtag}>#TryHackMe</Text>
        </Text>
        <Text style={styles.commentsLink}>View all 2 comments</Text>

        {/* Comments */}
        <View style={styles.comment}>
          <Text style={styles.commentUser}>Syam </Text>
          <Text>Congratulations 👏🎉👏🎉</Text>
        </View>
        <View style={styles.comment}>
          <Text style={styles.commentUser}>Sita </Text>
          <Text>Keep it up 💪👍, Congratulations 🎉 Amrit</Text>
        </View>

        {/* Post Time */}
        <Text style={styles.timestamp}>10 days ago</Text>
      </View>

      {/* Footer Icons */}
      <View style={styles.footer}>
        <Ionicons name="heart-outline" size={24} color="black" style={styles.footerIcon} />
        <Ionicons name="chatbubble-outline" size={24} color="black" style={styles.footerIcon} />
        <Ionicons name="paper-plane-outline" size={24} color="black" style={styles.footerIcon} />
        <Ionicons name="bookmark-outline" size={24} color="black" style={styles.footerIconRight} />
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    backgroundColor: '#fff',
    padding: 10,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  profileImage: {
    width: 40,
    height: 40,
    borderRadius: 20,
    marginRight: 8,
  },
  headerTextContainer: {
    flex: 1,
  },
  username: {
    fontWeight: 'bold',
    fontSize: 16,
  },
  followers: {
    fontSize: 12,
    color: 'gray',
  },
  verifiedIcon: {
    marginLeft: 4,
  },
  moreIcon: {
    marginLeft: 'auto',
  },
  postImage: {
    width: '100%',
    height: 400,
    borderRadius: 10,
    overflow: 'hidden',
    objectFit: 'cover',
  },
  imageOverlay: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.1)',
  },
  imageOverlay2: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(190, 190, 190, 1)',
  },
  certificateTitle: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 18,
  },
  certificateSubtitle: {
    color: '#fff',
    fontSize: 14,
    marginTop: 4,
  },
  content: {
    paddingVertical: 10,
  },
  caption: {
    fontSize: 14,
    lineHeight: 20,
  },
  hashtag: {
    color: '#00376b',
  },
  commentsLink: {
    color: 'gray',
    marginTop: 6,
  },
  comment: {
    flexDirection: 'row',
    marginTop: 4,
  },
  commentUser: {
    fontWeight: 'bold',
  },
  timestamp: {
    color: 'gray',
    fontSize: 12,
    marginTop: 8,
  },
  footer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 10,
  },
  footerIcon: {
    marginRight: 10,
  },
  footerIconRight: {
    marginLeft: 'auto',
  },
});

export default InstagramPostCard;
