import { Stack, Box } from "@mui/material";
import { VideoCard, ChannelCard } from ".";
import CardSkeleton from "./CardSkeleton";
// Need to get params
import { useParams } from "react-router-dom";
import { useState } from "react";
import { useEffect } from "react";
import { fetchFromAPI } from "../utils/fetchFromAPI";
import VideoDeailsSkeleton from "./VideoDeailsSkeleton";
import SkeletonCard from './SkeletonCard';

function Videos({ videos, direction }) {
  let pram = useParams();
  if (!videos?.length) return <CardSkeleton direction={direction} />;
  let [samay, setSamay] = useState();

  useEffect(() => {
    if (pram && pram.searchTerm == "class 12th physics") {
      fetchFromAPI(`search?part=snippet&q=physics parody`).then((data) =>
        setSamay(data.items)
      );
    }

  }, []);
  console.log(samay);
  if (pram && pram.searchTerm == "class 12th physics" && !samay) return <VideoDeailsSkeleton />;

  return (
    <Stack
      direction={direction || "row"}
      flexWrap='wrap'
      justifyContent='center'
      alignItems='center'
      gap={2}
    >
      {videos.map((item, index) => {
        if (pram && pram.searchTerm == "class 12th physics" && (index%5==0 && index!=0 && index!=1)) {
          console.log("Working")
          return <Box key={index}>
            {samay[index].id.videoId && <VideoCard video={samay[index]} />}
            {samay[index].id.channelId && <ChannelCard channelDetail={samay[index]} />}
          </Box>
          
        }
        else if(pram && pram.searchTerm == "class 11th physics" && (index%5==0 && index!=0 && index!=1)){
            return <SkeletonCard/>
        }
        else {
          return <Box key={index}>
            {item.id.videoId && <VideoCard video={item} />}
            {item.id.channelId && <ChannelCard channelDetail={item} />}
          </Box>
        }
      })}
    </Stack>
  );
}
export default Videos;
