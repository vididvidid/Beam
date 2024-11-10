import {
  View,
  Text,
  Image,
  TouchableOpacity,
  TextInput,
  ScrollView,
} from "react-native";
import * as ImagePicker from "expo-image-picker";
import { useState } from "react";
import IGButton from "../../components/custom/IGButton";
import useInput from "../../hooks/useInput";

export default function ProfileScreen() {
  const [image, setImage] = useState<string | null>(null);
  const [usernameProps] = useInput("");
  const [emailProps] = useInput("");
  const [websiteProps] = useInput("");

  const pickImage = async () => {
    // No permissions request is necessary for launching the image library
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.All,
      allowsEditing: true,
      aspect: [1, 1],
      quality: 1,
    });

    if (!result.canceled) {
      setImage(result.assets[0].uri);
    }
  };

  return (
    <ScrollView className="p-3 flex-1">
      {/* image picker for avatar */}
      {image ? (
        <Image
          source={{ uri: image }}
          className="w-64 aspect-square rounded-full self-center shadow-lg my-5"
        />
      ) : (
        <View className="w-64 aspect-square rounded-full self-center shadow-lg my-5 bg-slate-400" />
      )}

      <TouchableOpacity onPress={pickImage} className="self-center">
        <Text className="text-blue-500 font-semibold text-lg">Change</Text>
      </TouchableOpacity>

      {/* form */}
      <View className="mx-3 my-2">
        <Text className="mb-3 text-gray-500 font-semibold">Username</Text>
        <TextInput
          {...usernameProps}
          placeholder="Please enter your username"
          className="p-3 border-2 border-gray-300 rounded-md px-3 text-gray-700 font-medium"
        />
      </View>

      <View className="mx-3 my-2">
        <Text className="mb-3 text-gray-500 font-semibold">Email</Text>
        <TextInput
          {...emailProps}
          placeholder="Please enter your email"
          className="p-3 border-2 border-gray-300 rounded-md px-3 text-gray-700 font-medium"
        />
      </View>

      <View className="mx-3 my-2">
        <Text className="mb-3 text-gray-500 font-semibold">Website</Text>
        <TextInput
          {...websiteProps}
          placeholder="Please enter your website"
          className="p-3 border-2 border-gray-300 rounded-md px-3 text-gray-700 font-medium"
        />
      </View>

      {/* button */}
      <View className="mt-5 mx-3 gap-3">
        <IGButton title="Update Profile" />
        <IGButton title="Sign Out" />
      </View>
    </ScrollView>
  );
}
