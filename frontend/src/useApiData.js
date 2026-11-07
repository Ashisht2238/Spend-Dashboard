import { useEffect, useState } from "react";
import { getJson } from "./api";

export function useApiData(path, filters) {
  const [state, setState] = useState({ data: null, error: "" });

  useEffect(() => {
    let ignore = false;
    getJson(path, filters)
      .then((data) => {
        if (!ignore) {
          setState({ data, error: "" });
        }
      })
      .catch(() => {
        if (!ignore) {
          setState({ data: null, error: "Could not load this chart." });
        }
      });
    return () => {
      ignore = true;
    };
  }, [path, filters]);

  return state;
}   