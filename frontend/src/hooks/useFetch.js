import { ref } from "vue";
import config from "@/config";

const useFetch = async (url, options = {}) => {
  const data = ref(null);
  const error = ref(null);

  try {
    const response = await fetch(config.apiUrl + url, options);

    if (!response.ok) {
      await response.json().then((data) => {
        throw new Error(data.error);
      });
    }

    const result = await response.json();
    data.value = result;
  } catch (err) {
    error.value = err.message;
  }

  return {
    data,
    error,
  };
};

export default useFetch;
