import { Tabs } from "expo-router";
import { FontAwesome } from "@expo/vector-icons";
import { BottomNavigation } from "../../constants/bottomNavigation";

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarShowLabel: false,
        tabBarActiveTintColor: BottomNavigation.activeIconColor,
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          headerTitle: "For You",
          tabBarIcon: ({ color }) => (
            <FontAwesome
              name="home"
              size={BottomNavigation.defaultIconSize}
              color={color}
            />
          ),
        }}
      />

      <Tabs.Screen
        name="new"
        options={{
          headerTitle: "Create Post",
          tabBarIcon: ({ color }) => (
            <FontAwesome
              name="plus-square-o"
              size={BottomNavigation.defaultIconSize}
              color={color}
            />
          ),
        }}
      />

      <Tabs.Screen
        name="profile"
        options={{
          headerTitle: "Profile",
          tabBarIcon: ({ color }) => (
            <FontAwesome
              name="user-circle-o"
              size={BottomNavigation.defaultIconSize}
              color={color}
            />
          ),
        }}
      />
    </Tabs>
  );
}
