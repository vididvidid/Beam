import { TouchableOpacity, Text } from "react-native";

type IGButtonProps = {
  title: string;
  onPress?: () => void;
};

export default function IGButton({ title, onPress }: IGButtonProps) {
  return (
    <TouchableOpacity
      onPress={onPress}
      className="bg-blue-500 w-full p-3 rounded-lg items-center"
    >
      <Text className="text-white font-semibold text-lg">{title}</Text>
    </TouchableOpacity>
  );
}
