import { useState } from "react";

type IUseInput = [props: InputProps, reset: Function];

type InputProps = {
  value: string;
  onChangeText: (text: string) => void;
};

export default function useInput(initialValue: string): IUseInput {
  const [value, setValue] = useState<string>(initialValue);

  return [
    { value, onChangeText: (newValue: any) => setValue(newValue) },
    () => setValue(initialValue),
  ];
}
