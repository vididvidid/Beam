import React, { useState } from 'react';
import { FlatList, Dimensions } from 'react-native';
import PostCard from '../../components/post/PostCard';
import posts from '../../../assets/data/posts.json';

export default function FeedScreen() {
  const [isThirdImageCentered, setIsThirdImageCentered] = useState(false);
  const screenWidth = Dimensions.get('window').width;

  const handleScroll = (event) => {
    console.log("Scrolling");
    console.log(event.nativeEvent);
    const scrollPosition = event.nativeEvent.contentOffset.y;

    // Assuming each post has a fixed height of 250px, adjust if necessary
    const itemCenterPosition = (400 + 10) * 2 - screenWidth / 2; // Adjust for image height and padding

    if ((scrollPosition>900 && scrollPosition<1600) || (scrollPosition>2140 && scrollPosition<2800)) {
      setIsThirdImageCentered(true);
    }
    else{
      setIsThirdImageCentered(false);
    }
  };

  return (
    <FlatList
      onScroll={handleScroll}
      scrollEventThrottle={16}
      data={posts}
      className="bg-slate-200"
      renderItem={({ item }) => (
        <PostCard 
          key={item.id}
          post={item} 
          isThirdImageCentered={isThirdImageCentered}  // Pass the state to PostCard
        />
      )}
      contentContainerStyle={{ gap: 2 }}
      showsVerticalScrollIndicator={false}
    />
  );
}
