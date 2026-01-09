import { useEffect, useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000/api";

type ApiState<T> = {
  data: T[];
  loading: boolean;
  error: string | null;
};

export function useApi<T>(path: string) {
  const [state, setState] = useState<ApiState<T>>({
    data: [],
    loading: true,
    error: null
  });

  useEffect(() => {
    let active = true;
    setState({ data: [], loading: true, error: null });

    fetch(`${API_BASE}${path}`)
      .then(async (response) => {
        if (!response.ok) {
          throw new Error("No se pudo cargar la información");
        }
        return response.json() as Promise<T[]>;
      })
      .then((data) => {
        if (active) {
          setState({ data, loading: false, error: null });
        }
      })
      .catch((error: Error) => {
        if (active) {
          setState({ data: [], loading: false, error: error.message });
        }
      });

    return () => {
      active = false;
    };
  }, [path]);

  return state;
}
