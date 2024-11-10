import { useEffect, useState } from "react";
import { View, Text, Image, TouchableOpacity, TextInput } from "react-native";
import * as ImagePicker from "expo-image-picker";
import IGButton from "../../components/custom/IGButton";
import useInput from "../../hooks/useInput";

export default function CreateNewScreen() {
  const [captionProps] = useInput("");
  const [image, setImage] = useState<string | null>(null);

  const pickImage = async () => {
    // No permissions request is necessary for launching the image library
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.All,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    if (!result.canceled) {
      setImage(result.assets[0].uri);
    }
  };

  useEffect(() => {
    if (!image) {
      pickImage();
    }
  }, [image]);

  return (
    <View className="p-2 items-center flex-1">
      {/* image picker */}
      {image ? (
        <Image
          source={{ uri: image }}
          className="w-64 aspect-[3/4] rounded-lg shadow-lg my-5"
        />
      ) : (
        <View className="w-64 aspect-[3/4] rounded-lg shadow-lg my-5 bg-slate-400 items-center justify-center px-10">
          <Text className="text-gray-100 font-semibold text-xl text-wrap">
            Please select an image to post
          </Text>
        </View>
      )}

      <TouchableOpacity onPress={pickImage}>
        <Text className="text-blue-500 font-semibold text-lg">Change</Text>
      </TouchableOpacity>

      {/* text input for caption */}
      <TextInput
        {...captionProps}
        placeholder="What's on your mind"
        className="w-[90%] p-3"
      />

      {/* submit button */}
      <View className="mt-auto mb-5 w-[90%]">
        <IGButton title={"Share"} />
      </View>
    </View>
  );
}
